from socket import *
import sys
serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
serverSocket = socket(AF_INET, SOCK_STREAM);
serverSocket.bind((serverIP, serverPort));

#server begins listening for incoming TCP requests
serverSocket.listen(1);
print('Server is ready to receive');

while True:
    connectionSocket, addr = serverSocket.accept();
    recvMessage = connectionSocket.recv(1024).decode();
    capsSentence = recvMessage.upper();
    connectionSocket.send(capsSentence.encode());
    connectionSocket.close();