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
    while True:
        getUserOptions = True;
        clientSocket.send('GET_BOARDS'.encode());
        boardList = clientSocket.recv(1024);
        if pickle.loads(boardList) == 100:
            printError(100);
            getUserOptions = False;
        elif pickle.loads(boardList) == 101:
            printError(101);
            getUserOptions = False;
            break;
        else:
            fBoardList = formatBoardList(boardList);
            print('Boards retrieved successfully! \n Message boards: ', fBoardList);
        while True and getUserOptions == True:
            inputError = True;
            while inputError == True:
                inputError = False;
                userSelect = input('Input: \n - A board number \n - POST to post a message \n - QUIT \n');
                if userSelect == "QUIT":
                    print("quit");
                    clientSocket.close();
                    sys.exit();
                elif userSelect == "POST":
                    print("post");
                elif userSelect in range (1, (len(fBoardList)+1)):
                    print("board number selected");
                else:
                    print("ERROR: Invalid input, try again")
                    inputError == True;



finally:
    clientSocket.close();
    sys.exit();



