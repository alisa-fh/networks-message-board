from socket import *
import sys
import os
import pickle
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
    if recvMessage == "GET_BOARDS":
        boardList = os.listdir("./board");
        boardListToSend = pickle.dumps(boardList);
        print(boardList);
        connectionSocket.send(boardListToSend);
    else:
        sendMessage = "did not receive";
        connectionSocket.send(sendMessage.encode());
    connectionSocket.close();