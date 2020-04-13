from socket import *
from getpass import getpass

#Receive List of Username and passwords if login
#Send new user details if register
#if login 

#Functions
def mainmenu():
    print("-----------Cloud Storage----------")
    print("1-Login\n2-Regster\n3-Exit")
    print("Enter Your Choice")
    choice=input()
    if(choice=="1"):
        loginmenu()
    elif(choice=="2"):
        print("--------Registration Menu-----------")
        regmenu()
    elif(choice=="3"):
        clientSocket.send("quit".encode())
        print("Thank You")
        exit(1)
    else:
        print("Invalid Input.Please Try Again")

def loginmenu():
    global uname
    global clientSocket
    global serverName,serverPort
    global login
    #clientSocket.connect((serverName,serverPort))
    print("Enter Username")
    uname=input()
    print("Enter Password")
    pswd=getpass()
    sen="login "+uname+" "+pswd
    clientSocket.send(sen.encode())
    sen=clientSocket.recv(1024).decode()
    #clientSocket.close()
    if(sen=="1"):
        login=1
    else:
        print("Login Unsuccessful. Please Try Again")
        loginmenu()

def regmenu():
    global clientSocket
    global serverName,serverPort
    global login
    global uname
    #clientSocket.connect((serverName,serverPort))
    print("Enter username")
    runame=input()
    if(runame=="admin"):
        print("Username already taken.")
        regmenu()
    print("Enter password")
    rpswd=getpass()
    print("Re-Enter Password")
    reprpswd=getpass()
    if(rpswd!=reprpswd):
        print("Passwords do not match. Please Try Again!")
        regmenu()
    else:
        sen="register"+" "+runame+" "+rpswd
        clientSocket.send(sen.encode())
    signal = clientSocket.recv(1024).decode()
    if(signal == "1"):
        print("Username already taken. Try again")
        regmenu()
    else:
        print("Successfully registerred")
        uname = runame
        login = 1
        usermenu()
        #clientSocket.close()
    #Send username and password to server
    
def usermenu():
    global login
    global uname
    global clientSocket
    print("-------------USER Menu-----------")
    print("1-Upload a file\n2-List your files\n3-Logout")
    choice=input()
    if(choice=="1"):
        print("\nPlease Enter the name of the file and the entire path")
        fle=input().split(" ")
        if(fle[1][0] == "\'"):
            fle[1] = fle[1][1:-1]
        s="Logged "+uname+" Sending "+fle[0]
        clientSocket.send(s.encode())
        #print(fle[0])
        anc=clientSocket.recv(1024).decode()
        if(anc=="Success"):
            x=open(fle[1],"r")
            content=x.read()
            clientSocket.send(content.encode())
        else:
            print(anc)
            usermenu()
    elif(choice=="2"):
        sen="Logged "+uname+" list"
        clientSocket.send(sen.encode())
        listoutput=clientSocket.recv(1024).decode()
        if(listoutput=="empty"):
            print("Directory Empty")
            usermenu()
        else:
            print("\n"+listoutput)
            print("\n"+"Enter the filename to view it.Enter 'return' to go the menu",end=":")
            viewfle=input()
            if(viewfle!="return"):
                viewfle="Logged "+uname+" View "+viewfle
                clientSocket.send(viewfle.encode())
                op=clientSocket.recv(1024).decode()
                print("\n   ##########################################\t")
                print("\n"+op+"\n")
                print("   ##########################################\t\n")
    elif(choice=="3"):
        print("logout Successful")
        login=0

#MAIN 
uname=" "
serverName='127.0.0.1'
serverPort=12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print("Connection Successful")
login=0
uname=0
while(1):
    if(login==0):
        mainmenu()
    elif(login==1):
        usermenu()

