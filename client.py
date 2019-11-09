from socket import *
import sys
serverIP = (sys.argv[1]);
serverPort = int(sys.argv[2]);
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket.connect((serverIP, serverPort));
sentence = input('Input a lower case sentence ');
clientSocket.send(sentence.encode());
modifiedSentence = clientSocket.recv(1024);
print('From server: ', modifiedSentence.decode());
clientSocket.close();
