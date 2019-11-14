from socket import *
import errno
import sys
import os
import pickle
serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
serverSocket = socket(AF_INET, SOCK_STREAM);

try:
    serverSocket.bind((serverIP, serverPort));
    portConnected = True;
except error as e:
        print("Port is unavailable");
        print("Specific error: " + str(e));
        portConnected = False;
        serverSocket.close();

#server begins listening for incoming TCP requests
if portConnected:
    serverSocket.listen(1);
    print('Server is ready to receive');

    while True:
        connectionSocket, addr = serverSocket.accept();
        recvMessage = connectionSocket.recv(1024).decode();

        try:
            if recvMessage:
                if recvMessage == "GET_BOARDS":
                    boardList = os.listdir("./board");
                    for item in boardList:
                        if item[0] == '.':
                            boardList.remove(item);
                    boardListToSend = pickle.dumps(boardList);
                    print(boardList);
                    connectionSocket.send(boardListToSend);
                else:
                    sendMessage = 100;
                    connectionSocket.send(pickle.dumps(sendMessage));
        finally:
            connectionSocket.close();