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
        print("ERROR: Port is unavailable");
        print("Specific error: " + str(e));
        portConnected = False;
        serverSocket.close();

#server begins listening for incoming TCP requests
if portConnected:
    serverSocket.listen(1);
    print('Server is ready to receive');
    connectionSocket, addr = serverSocket.accept();
    print("Connection from: " + str(addr));
    while True:
        recvMessage = connectionSocket.recv(1024).decode();
        if recvMessage:
            if recvMessage == "GET_BOARDS":
                boardList = os.listdir("./board");
                for item in boardList:
                    if item[0] == '.':
                        boardList.remove(item);
                if len(boardList) == 0:
                    print("ERROR: No message boards defined");
                    connectionSocket.send(pickle.dumps(101));
                    serverSocket.close()
                    break;
                boardListToSend = pickle.dumps(boardList);
                print(boardList);
                connectionSocket.send(boardListToSend);
            else:
                sendMessage = 100;
                connectionSocket.send(pickle.dumps(sendMessage));
        else:
            break;
    connectionSocket.close();