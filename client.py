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

def getMessages(boardIndex, boardList):
    boardName = boardList[boardIndex].split()[1];
    clientSocket.send(('GET_MESSAGES('+boardName+')').encode());
    rtnMsg = pickle.loads(clientSocket.recv(1024));
    return rtnMsg;

def postMessage(numBoards):
    boardNumError = True;
    while boardNumError == True:
        boardNum = int(input("Select the number of the board to write to: \n"));
        if (boardNum > 0) and (boardNum <= numBoards):
            boardNumError = False;
    msgName = input("Title of your message: \n")
    msgName = msgName.replace(' ', '_');
    msgContents = input("Content of your message: \n");
    sendData = 'POST_MESSAGE' + '\n' + str(boardNum) + '\n' + msgName + '\n' + msgContents;
    clientSocket.send(sendData.encode());
    status = pickle.loads(clientSocket.recv(1024));
    return status;


serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket.connect((serverIP, serverPort));
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
    while getUserOptions == True:  # instead of while True
        inputError = True;
        while inputError == True:
            inputError = False;
            userSelect = input('Input: \n - A board number \n - POST to post a message \n - QUIT \n');
            if userSelect == "QUIT":
                print("quit");
                clientSocket.close();
                sys.exit();
            elif userSelect == "POST":
                returnData = postMessage(len(fBoardList));
                print(returnData);
            elif int(userSelect) in range(1, (len(fBoardList) + 1)):
                print("board number selected");
                displayMsg = getMessages((int(userSelect) - 1), fBoardList);
                if displayMsg == []:
                    print('No messages yet in this board');
                else:
                    print('Latest Messages From This Board: ', displayMsg);
            else:
                print("ERROR: Invalid input, try again")
                inputError == True;



clientSocket.close();
sys.exit();



