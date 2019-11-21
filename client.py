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
        print("ERROR: Invalid Request sent");
    if errorVal == 101:
        print("ERROR: No message boards have been defined");

def getMessages(boardNum):
    try:
        clientSocket.send(('GET_MESSAGES('+boardNum+')').encode());
        rtnMsg = pickle.loads(clientSocket.recv(1024));
    except timeout:
        timeoutError();
    return rtnMsg;

def postMessage(numBoards):
    boardNumError = True;
    dispErr = 0;
    while boardNumError == True:
        if dispErr == 1:
            print("ERROR: Not a valid board number. Try again.");
        boardNum = int(input("Select the number of the board to write to: \n"));
        if (boardNum > 0) and (boardNum <= numBoards):
            boardNumError = False;
        else:
            dispErr = 1;
    msgName = input("Title of your message: \n")
    msgName = msgName.replace(' ', '_');
    msgContents = input("Content of your message: \n");
    sendData = 'POST_MESSAGE' + '\n' + str(boardNum) + '\n' + msgName + '\n' + msgContents;
    try:
        clientSocket.send(sendData.encode());
        status = pickle.loads(clientSocket.recv(1024));
    except timeout:
        timeoutError();
    return status;

def timeoutError():
    print("ERROR: The server timed out");
    clientSocket.close();
    sys.exit();



serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket.settimeout(10);

result = clientSocket.connect_ex((serverIP, serverPort));
if result != 0:
    print("ERROR: Server is not running on this port. ");
    clientSocket.close();
    sys.exit();

while True:
    getUserOptions = True;
    try:
        clientSocket.send('GET_BOARDS'.encode());
        boardList = clientSocket.recv(1024);
    except timeout:
        timeoutError();
    if pickle.loads(boardList) == 100:
        printError(100);
    elif pickle.loads(boardList) == 101:
        printError(101);
        getUserOptions = False;
        break;
    elif isinstance(pickle.loads(boardList), list) == True:
        fBoardList = formatBoardList(boardList);
        print('Boards retrieved successfully! \n Message boards: ');
        for item in fBoardList:
            print(item);
    else:
        print('ERROR: ', pickle.loads(boardList));
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
                if returnData == 100:
                    printError(100);
                else:
                    print(returnData);
            elif userSelect.isdigit():
                displayMsg = getMessages(userSelect);
                if displayMsg == 100:
                    printError(100);
                elif displayMsg == 102:
                    print("ERROR: Input is not a board number");
                    inputError = True;
                elif displayMsg == []:
                    print('No messages yet in this board');
                elif displayMsg[:5] == "ERROR":
                    print(displayMsg);
                else:
                    print('Successful Retrieval of Messages!');
                    print('Latest Messages From This Board: ');
                    for message in displayMsg:
                        print(message);
            else:
                print("ERROR: Invalid input, try again")
                inputError = True;



clientSocket.close();
sys.exit();



