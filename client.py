from socket import *
import sys
import pickle

def formatBoardList(aBoardList):
    aBoardList = pickle.loads(boardList);
    for i in range(len(aBoardList)):
        aBoardList[i] = str(i+1) + '. ' + aBoardList[i];
    return aBoardList;

def printError(errorVal):
    if errorVal == 100:
        print("Invalid Request sent");
    if errorVal == 101:
        print("No message boards have been defined");


serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket.connect((serverIP, serverPort));
try:
    clientSocket.send('GET_BOARDS'.encode());
    boardList = clientSocket.recv(1024);
    if pickle.loads(boardList) == 100:
        printError(100);
    elif pickle.loads(boardList) == 101:
        printError(101);
    else:
        fBoardList = formatBoardList(boardList);
        print('Message boards: ', fBoardList);
finally:
    clientSocket.close();



