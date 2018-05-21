# Authors: Tushar Pahuja, Pragam Manoj Gandhi
# importing corresponding Dependencies
import socket
# socket for TCP connection establishment
import threading
# threading for allowing multiple client connections
import os
# OS to find a file
import shlex
# shlex for lexical analysis


HOST=''
IP=''
PORT=0
rfc_list=list()
rfc_title=list()

a_list=list()

class RFCRecord:
    def __init__(self,rfc_number=-1,rfc_title='None'):
        self.rfc_number=rfc_number
        self.rfc_title=rfc_title

    def __str__(self):
        return str(self.rfc_number)+' '+str(self.rfc_title)

    def getRFCNumber(self):
        return self.rfc_number


def requestRFC(message,rfc_number,peer_name,peer_port,file_name):
    client_socket=socket.socket()
    
    peer_ip=peer_name
    #denoting peer's IP address	
    client_socket.connect((peer_ip,peer_port))
    print "*"*20
    print "client successfully connected"
    print "*"*20
    # sending messsage through socket
    client_socket.send(message)
    # receiving reply form server	
    reply=client_socket.recv(1024)
    
   
    reply_list=shlex.split(reply)
    os.chdir(os.getcwd())
    file_name=file_name+".txt"
    #print str(file_name)
    if str(reply_list[1])=='200':
        #open the file here
        file1=open(file_name,'wb')
        while True:
            q=client_socket.recv(1024)
            if q:
                #print q
                file1.write(q)
                break
            else:
                file1.close()
                break
    else:
        print "File Not Found"
    client_socket.close()


def RetrRFC(name, sock):
    # wating for peer's response
    request=sock.recv(1024)
    print request
    # extracting the rfc_number from the received request of the peer
    rfc_number=shlex.split(request)
    # using a flag to identify if the requested RFC is present
    file_found = 0
    for x in a_list:
        #Searching through the available RFC's that are present in the list named a
        t = x.split("-")
        if int(t[0])==int(rfc_number[2]):
            print t[0]
	    print "file found"
            file_found=1
            file_name=str(x)+".txt"

    if file_found==0:
        print "File was not found"
        file_data="P2P-CI/1.0 404 FILE NOT FOUND"+"\n"
        sock.send(file_data)
    else:
	print "File Found"
        file_data="P2P-CI/1.0 200 OK"+"\n"
        sock.send(file_data)
        try:
            with open(file_name,'r') as temp:
                bytesRequiredToSend = temp.read(1024)
                sock.send(bytesRequiredToSend)
                # COntinue to send till the data is being received at the socket 
    	    while bytesRequiredToSend != "":
                    bytesRequiredToSend = temp.read(1024)
                    sock.send(bytesRequiredToSend)
        except:
            print 'successful'
 
    sock.close()


def RetrRFC_initial():
    s=socket.socket()
    s.bind(('127.0.0.0',5000))
    s.listen()
    while True:
        c,addr = s.accept()
        print "Client connected ip: "+str(addr)
        t=threading.Thread(target=RetrRFC,args=("retrThread",c))
        t.start()
    s.close()
    

def initial_rfc_add():
    global a_list
    # listing the files present
    file_list = os.listdir(os.getcwd())
    # initialising with empty list
    temp_rfc_list = list()
    temp_title_list = list()
    for file_name in file_list:
        #print file_name and file directory
        files = file_name.split(".")
	# checking for a text file after split and getting the extension
        if files[1] == "txt":
            w = str(files[0])
            a_list.append(w)
            files1 = w.split("-")
            temp_rfc_list.append(int(files1[0]))
            temp_title_list.append(files1[1])
    return temp_rfc_list,temp_title_list
   
    

def file_send(self):
    request=self.recv(1024)
    print request
    rfc_number=shlex.split(request)
    file_name=str(rfc_number[2])+".txt"
    for x in a_list:
        print x

    if str(rfc_number[2]) not in a_list:
        print "File not found"
        file_data="P2P-CI/1.0 404 FILE NOT FOUND"+"\n"
        self.send(file_data)
    else:
        data=subprocess.check_output(['date'])
        uname=subprocess.check_output(['uname'])
        t1=['ls','-lrt']
        t2=['grep','-w',file_name]
        t3=['tr','-s','" "']
        t4=['awk','{print $6,$7,$8}']
        t12=['ls','-lrt']
        t22=['grep','-w',file_name]
        t32=['tr','-s','" "']
        t42=['awk','{print $5}']
        p1=subprocess.Popen(t1,stdout=subprocess.PIPE)
        p2=subprocess.Popen(t2,stdin=p1.stdout,stdout=subprocess.PIPE)
        p3=subprocess.Popen(t3,stdin=p2.stdout,stdout=subprocess.PIPE)
        p4=subprocess.Popen(t4,stdin=p3.stdout,stdout=subprocess.PIPE)
        p3.stdout.close()
        lastupdate=p4.communicate()
        print lastupdate

        p12=subprocess.Popen(t12,stdout=subprocess.PIPE)
        p22=subprocess.Popen(t22,stdin=p12.stdout,stdout=subprocess.PIPE)
        p32=subprocess.Popen(t32,stdin=p22.stdout,stdout=subprocess.PIPE)
        p42=subprocess.Popen(t42,stdin=p32.stdout,stdout=subprocess.PIPE)
        p32.stdout.close()
        file_size=p42.communicate()
        print file_size

        f=open(file_name,'r')
        file_data="P2P-CI/1.0 200 OK"+"\n"+"Date: "+str(date)+"\n"+"OS: "+uname+"\n"+"Last-Modified: "+lastupddate[0]+"\n"+"Content-Length: "+str(file_size[0])+"\n"+"Content-Type: text/text"+"\n"
        self.send(file_data)

        stat=self.recv(1)

        while True:
            line=f.read(1024)
            self.send(line)
            if not len(line):
                break

        f.close()
    return 0       
    


def main():

    # Referencing the global variables
    global IP

    global PORT

    global HOST

    
    
    print "Enter IP address of the host(your's)"
    IP=raw_input()
    print "Enter Host(your's) name"
    HOST=raw_input()
    #HOST=socket.gethostbyname()
    print "Enter Your Upload Port number"
    PORT=int(raw_input())
    #initial_rfc_add()
    try:
    	# instantiating the thread with target as client_as_server method
        thread_first = threading.Thread(target=client_as_server)
	# Instantiating the second thread with target as option_list
        thread_second = threading.Thread(target=option_list)
	# using daemon threads
        thread_first.daemon=True
        thread_second.daemon=True
	# starting both the threads
        thread_first.start()
        thread_second.start()
	# using join so that the program waits for the threads to complete
        thread_first.join()
        thread_second.join()

    except KeyboardInterrupt:
        sys.exit(0)


def client_as_server():

    # creating a socket at the client side which will act as a server when a peer requests a RFC
    clients_server_socket = socket.socket()
    clients_server_ip=IP
    clients_server_port=PORT
    clients_server_socket.bind((clients_server_ip,clients_server_port))
    
    # Queue size for requests is 2
    clients_server_socket.listen(2)

    clients_server_thread = threading.current_thread()
    while(1):
	
	# getting the connection details
        (peer_socket,peer_addr)=clients_server_socket.accept()
        print "Connected to", peer_addr, "with socket as", peer_socket
        thread_third=threading.Thread(target=RetrRFC,args=("retrThread",peer_socket))
        thread_third.start()
        thread_third.join()
    clients_server_socket.close()
    return




def client(message, serverIP, serverPort):
    # Creating a scoket that sends and receives data from the server
    c_sock = socket.socket()
    c_sock.connect((serverIP,serverPort))
    c_sock.send(message)
    reply=c_sock.recv(16384)
    print "*"*30
    print "Response Received from the Server: with IP Address: ", serverIP, "and Port Number: ",serverPort
    print reply
    print "*"*30
    # closing the socket when data transmission complete
    c_sock.close()




def listALLRFCS(serverIP,serverPort):
    # For listing all the RFC's
    message="LISTALL P2P-CI/1.0"+"\n"+"Host: "+HOST+"\n"+" Port: "+str(PORT)
    client(message,serverIP,serverPort)
    return



def lookupRFCS(serverIP,serverPort):
    # for searching for a RFC
    print "Enter RFC number"
    rfc_number = int(raw_input())
    print "Enter RFC title"
    rfc_title=raw_input()
    message="LOOKUP"+" "+str(rfc_number)+" P2P-CI/1.0"+"\n"+"Host: "+HOST+"\n"+"Port: "+str(PORT)+"\n"+"Title:"+rfc_title
    client(message,serverIP,serverPort)
    return

def addRFCS(serverIP,serverPort):
        # Adding an RFC
    print "Enter RFC number"
    rfc_number=raw_input()
    print "Enter the title for the RFC"
    rfc_title=raw_input()
    a_list.insert(0,str(rfc_number))
    message="ADD"+" "+rfc_number+" P2P-CI/1.0"+"\n"+" Host: "+HOST+"\n"+" Port: "+str(PORT)+"\n"+" Title: "+rfc_title
    client(message,serverIP,serverPort)
    return

def getRFCS(serverIP,serverPort):
    # get an RFC
    print "Enter RFC number"
    rfc_number=int(raw_input())
    print "Enter the title for the RFC"
    rfc_title=raw_input()
    print "Enter Peer Name"
    name_peer=raw_input()
    print "Enter Peer port number"
    port_peer=int(raw_input()) 
    message="GET RFC"+" "+str(rfc_number)+" "+"P2P-CI/1.0"+"\n"+"Host: "+name_peer+"\n"+"OS: Windows"
    file_name=str(rfc_number)+"-"+rfc_title
    requestRFC(message,rfc_number,name_peer,port_peer,file_name)
    print "File: ",file_name," successfully received"
    return
    
    
def removeRFCS(serverIP,serverPort):
    # Remove an RFC  
    print "Enter RFC number"
    rfc_number = int(raw_input())
    print "Enter RFC title"
    rfc_title = raw_input()
    str_file_name = str(rfc_number)+"-"+rfc_title+".txt"
    os.remove(str_file_name)
    print "Removing File in Progress"
    message="REMOVE"+" "+str(rfc_number)+" P2P-CI/1.0"+"\n"+" Host: "+HOST+"\n"+" Port: "+str(PORT)+"\n"+" Title: "+rfc_title
    client(message, serverIP, serverPort)
    print "FIle removed Successfully"
    return

def exitCode(serverIP,serverPort):
    # Exit
    message="EXIT P2P-CI/1.0 Host: "+HOST+" Port: "+str(PORT)
    print "Terminating the Connection"
    client(message, serverIP, serverPort)
    return
    


def option_list():
    temp_rfc_list=list()
    temp_title_list=list()
    print "Enter Host name/IP of the Centralised Server"
    serverIP=raw_input()
    
    print "Enter Port number of the Centralised Server"
    # getting the port number of the server at which it is waiting for connections
    serverPort=int(raw_input())
    # Registering with the server
    message="REGISTER P2P-CI/1.0 Host: "+HOST+" Port: "+str(PORT)+"\n"
    client(message,serverIP,serverPort)
    # getting info of all the RFC's that we have
    temp_rfc_list, temp_title_list=initial_rfc_add()
    print temp_rfc_list
    for k in range(len(temp_rfc_list)):
        # temp_rfc_list[k]
        message="ADD"+" "+str(temp_rfc_list[k])+" P2P-CI/1.0"+"\n"+" Host: "+HOST+"\n"+" Port: "+str(PORT)+"\n"+" Title: "+temp_title_list[k]
        client(message,serverIP,serverPort)
    
    #myoptions = { 1 : listAllRFCS, 2 : lookupRFCS, 3 : addRFCS, 4 : getRFCS, 5 : removeRFCS, 6 : exitCode}
    while(1):
       
        print "Please select an option from the List displayed below"
            # Listing all the options
        print "1. List all RFC"
        print "2. Lookup an RFC"
        print "3. Add RFC"
        print "4. Get RFC "
        print "5. Remove a RFC"
        print "6. Exit"

        opt=int(raw_input())
        
        if opt == 1:
            listALLRFCS(serverIP,serverPort)

        if opt == 2:
            lookupRFCS(serverIP,serverPort)

        if opt == 3:
            addRFCS(serverIP,serverPort)
            
        if opt == 4:
            getRFCS(serverIP,serverPort)
            
        if opt == 5:
             removeRFCS(serverIP,serverPort)

        if opt == 6:
            exitCode(serverIP,serverPort)
        #func = options.get(opt)
        #myoptions[opt]()
        #self.func()   
       

        
          

    return            

if __name__=="__main__":
    main()
