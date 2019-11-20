from socket import *
import glob;
import sys;
import os;
import pickle;
import datetime;

def getMessages(aBoardList, aBoardNum):
    if aBoardNum > 0 and aBoardNum <= len(aBoardList):
        aBoardName = aBoardList[aBoardNum-1];
        thePath = os.getcwd() + '/board/'+ aBoardName +'/*';
        print(thePath);
        allFiles = glob.glob(thePath);
        sorted_files = sorted(allFiles, key=os.path.getctime);
        rtnMessages = [];
        i = 1;
        while i < 101 and i < len(sorted_files) + 1:
            with open(sorted_files[(i*-1)], "r") as aFile:
                data = aFile.read().replace('\n', ' ');
                aFile.close();
            rtnMessages.append(data);
            i += 1;
        return rtnMessages;
    else:
        return '102';

def postMessage(boardList, boardNum, msgTitle, msgContents):
    currentDT = (str(datetime.datetime.now())[:19]).replace(' ', '-').replace(':','');
    msgTitle = currentDT + '-' + msgTitle;
    aBoardName = boardList[int(boardNum)-1];
    thePath = os.getcwd() + '/board/' + aBoardName;
    completeFileName = os.path.join(thePath, msgTitle + '.txt');
    print('path ', completeFileName);
    try:
        aFile = open(completeFileName, 'w+');
        aFile.write(msgContents);
        aFile.close();
        return "Successfully Posted!";
    except error as e:
        print('an error has occurred');
        return "ERROR: details -" + e;

serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
serverSocket = socket(AF_INET, SOCK_STREAM);

try:
    serverSocket.bind((serverIP, serverPort));
    portConnected = True;
except error as e:
        print("ERROR: Port is unavailable");
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
                try:
                    boardList = os.listdir("./board");
                    for item in boardList:
                        if item[0] == '.':
                            boardList.remove(item);
                    if len(boardList) == 0:
                        print("ERROR: No message boards defined");
                        connectionSocket.send(pickle.dumps(101));
                        serverSocket.close();
                        break;
                    boardListToSend = pickle.dumps(boardList);
                    connectionSocket.send(boardListToSend);
                except error as e:
                    errorToSend = pickle.dumps(e);
                    connectionSocket.send(e);
                    serverSocket.close();
                    break;
            elif recvMessage[0:13] == "GET_MESSAGES(":
                boardNum = recvMessage[13:len(recvMessage)-1];
                rtnMessages = getMessages(boardList, int(boardNum));
                connectionSocket.send(pickle.dumps(rtnMessages));

            elif recvMessage.split('\n')[0] == "POST_MESSAGE":
                parameters = recvMessage.split('\n');
                status = postMessage(boardList, parameters[1], parameters[2], parameters[3]);
                connectionSocket.send(pickle.dumps(status));
            else:
                sendMessage = 100;
                connectionSocket.send(pickle.dumps(sendMessage));
        else:
            break;
    connectionSocket.close();