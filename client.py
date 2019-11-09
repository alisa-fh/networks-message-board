from socket import *
import sys
import pickle
serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket.connect((serverIP, serverPort));
clientSocket.send('GET_BOARDS'.encode());
boardList = clientSocket.recv(1024);
print('From server: ', pickle.loads(boardList));
clientSocket.close();
