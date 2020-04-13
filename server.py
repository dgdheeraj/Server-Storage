from socket import *
import os
import subprocess
import json

pwpath = "/home/dgdheeraj/Desktop/v2/pswd.txt"
fp = open(pwpath,"r")
pwtxt = fp.readline()
pwdict = json.loads(pwtxt)
fp.close()
serverPort=12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
while(1):
    connectionSocket, addr = serverSocket.accept()
    sentence='  '
    while(sentence[0]!="quit"):
        sentence = connectionSocket.recv(1024).decode().split(" ")
        if(sentence==''):
            sleep(1)
        print(sentence)
        if(sentence[0]=="login"):
            if pwdict[sentence[1]] == sentence[2]:
                connectionSocket.send("1".encode())
                print(sentence[1]," logged in")
            else:
                connectionSocket.send("2".encode())
                print("Wrong password for ",sentence[1])
        if(sentence[0]=="register"):
            if(sentence[1] in pwdict):
                print("Username already taken")
                connectionSocket.send("1".encode())   #1 - username taken
            else:
                pwdict[sentence[1]] = sentence[2]
                pwtxt = json.dumps(pwdict)
                wfp = open(pwpath,"w")
                wfp.write(pwtxt)
                wfp.close()
                connectionSocket.send("2".encode())   #2 - registered
                try:
                    os.mkdir(sentence[1])
                except FileExistsError:
                    print("Folder Exists")
#Logged username list->for listing files of username
        if(sentence[0]=="Logged"):
            u=sentence[1]
            direct='/home/dgdheeraj/Desktop/v2/'+sentence[1]
            if(sentence[2]=="list"):
                os.listdir(sentence[1])
                cmd='ls /home/dgdheeraj/Desktop/v2/'+sentence[1]
                #x=os.system('ls /home/suhas/Desktop/5th sem/CN/P3/'+sentence[1])
                myCmd = os.popen(cmd).read()
                if(len(myCmd)==0):
                    myCmd="empty"
                connectionSocket.send(myCmd.encode())
                print(myCmd)
            if(sentence[2]=="View"):
                #cmd='ls /home/suhas/Desktop/5th sem/CN/P3/'+sentence[1]+'/'+sentence[3]
                #mycmd=os.popen(cmd).read()
                #connectionSocket.send(mycmd.encode())
                cmd='cat /home/dgdheeraj/Desktop/v2/'+sentence[1]+'/'+sentence[3]
                #x=os.system('ls /home/suhas/Desktop/5th sem/CN/P3/'+sentence[1])
                try:
                    myCmd = os.popen(cmd).read()
                except:
                    myCmd="Error Occured. Please Try Again"
                connectionSocket.send(myCmd.encode())
                print(myCmd)
            if(sentence[2]=="Sending"):
                di=direct+'/'+sentence[3]
                print(di)
                if(os.path.exists('/home/dgdheeraj/Desktop/v2/'+sentence[1]+'/'+sentence[3])==False):
                    fle=open(di,"w+")
                    #while(1):
                    connectionSocket.send("Success".encode())
                    sen=connectionSocket.recv(1024).decode()
                        #if not sen:
                            #break
                    fle.write(sen)
                    fle.close()
                else:
                    a="File Already Exists"
                    connectionSocket.send(a.encode())



