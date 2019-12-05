from socket import *
import glob;
import sys;
import os;
import pickle;
import datetime;
from _thread import *;
import threading

def getMessages(aBoardList, aBoardNum):
    if aBoardNum > 0 and aBoardNum <= len(aBoardList):
        try:
            aBoardName = aBoardList[aBoardNum-1];
            thePath = os.getcwd() + '/board/'+ aBoardName +'/*';
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
        except error as e:
            return ('ERROR: ' + e);
    else:
        return 102;

def postMessage(boardList, boardNum, msgTitle, msgContents):
    currentDT = (str(datetime.datetime.now())[:19]).replace(' ', '-').replace(':','');
    msgTitle = currentDT + '-' + msgTitle;
    aBoardName = boardList[int(boardNum)-1];
    thePath = os.getcwd() + '/board/' + aBoardName;
    completeFileName = os.path.join(thePath, msgTitle + '.txt');
    try:
        aFile = open(completeFileName, 'w+');
        aFile.write(msgContents);
        aFile.close();
        return "Successfully Posted!";
    except error as e:
        print('an error has occurred');
        return "ERROR: details -" + e;

def serverLog(clientIPPort, msgType, status):
    currentDT = datetime.datetime.now().strftime("%c");
    completeFileName = os.path.join(os.getcwd(), 'serverLog.txt');
    try:
        serverLogFile = open(completeFileName, "a+");
        serverLogFile.write(clientIPPort + '\t' + currentDT + '\t' + msgType + '\t' + status + '\n');
        serverLogFile.close();
    except error as e:
        print('ERROR: serverLog error has occurred - ', e);

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
        os._exit(1);

#server begins listening for incoming TCP requests
serverSocket.listen(5);

def threaded(connectionSocket):
    print('new thread');
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
                        serverLog(formattedAddr, "GET_BOARDS", "Error");
                        serverSocket.close();
                        break;
                    boardListToSend = pickle.dumps(boardList);
                    connectionSocket.send(boardListToSend);
                    serverLog(formattedAddr, "GET_BOARDS", "Success");
                except error as e:
                    errorToSend = pickle.dumps(e);
                    connectionSocket.send(e);
                    serverLog(formattedAddr, "GET_BOARDS", "Error");
                    serverSocket.close();
                    break;
            elif recvMessage[0:13] == "GET_MESSAGES(":
                boardNum = recvMessage[13:len(recvMessage)-1];
                rtnMessages = getMessages(boardList, int(boardNum));
                connectionSocket.send(pickle.dumps(rtnMessages));
                if rtnMessages == 102:
                    serverLog(formattedAddr, "GET_MESSAGES", "Error");
                elif rtnMessages[:5] == "ERROR":
                    serverLog(formattedAddr, "GET_MESSAGES", "Error");
                else:
                    serverLog(formattedAddr, "GET_MESSAGES", "Success");

            elif recvMessage.split('\n')[0] == "POST_MESSAGE":
                parameters = recvMessage.split('\n');
                status = postMessage(boardList, parameters[1], parameters[2], parameters[3]);
                connectionSocket.send(pickle.dumps(status));
                if status == 'Successfully Posted!':
                    serverLog(formattedAddr, "POST_MESSAGE", "Success");
                elif status[:5] == "ERROR":
                    serverLog(formattedAddr, "POST_MESSAGE", "Error");
            else:
                sendMessage = 100;
                connectionSocket.send(pickle.dumps(sendMessage));
        else:
            break;
    return True;
    connectionSocket.close();

while True:
    print('Server is ready to receive');
    connectionSocket, addr = serverSocket.accept();
    formattedAddr = str(addr)[1:len(str(addr)) - 1].replace(', ', ':').replace("'", '');
    print("Connection from: " + str(addr));
    start_new_thread(threaded, (connectionSocket,))
connectionSocket.close();
serverSocket.close();