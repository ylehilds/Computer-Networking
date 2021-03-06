from socket import *

import sys
import _thread


def getFileName(request):
    return request.split()[1][1:]


def myThread(connectionSocket, addr):
    request = connectionSocket.recv(2048)
    fileName = getFileName(request.decode())
    try:
        with open(fileName, 'r') as f:
            outPutData = f.read()
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
            responce = header + outPutData
            connectionSocket.send(responce.encode())
        print('{} Request success'.format(addr))
    except IOError:
        print('{} request fail'.format(addr))
        connectionSocket.send('HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8'))
    finally:
        connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[1])
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print('The server is ready to receive...')
while True:
    connectionSocket, addr = serverSocket.accept()
    _thread.start_new_thread(myThread, (connectionSocket, addr))
