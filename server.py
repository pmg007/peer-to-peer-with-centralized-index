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

count=0
peer_list=list()
index_list=list()
rfcList=list()
    
# class for RFC record    
class RFCRecord:
    # constructor
    def __init__(self, rfc_number=-1, rfc_title='None', peerHostname='None', peerid=-1):
        self.rfc_number=rfc_number
        self.rfc_title=rfc_title
        self.peerHostname=peerHostname
        self.peerid=peerid

    def __str__(self):
        return str(self.rfc_number)+' '+str(self.rfc_title)+' '+str(self.peerHostname)+' '+str(self.peerid)

    def get_peer_id(self):
        return self.peerid

    def get_peer_host_name(self):
        return self.peerHostname

    def get_rfc_title(self):
        return self.rfc_title

# class for Peer record
class PeerRecord:
    # constructor
    def __init__(self,peerHostname='None',peerPortNo=10000,peerid=-1):
        self.peerHostname=peerHostname
        self.peerPortNo=peerPortNo
        self.peerid=peerid

    def __str__(self):
        return str(self.peerHostname)+' '+str(self.peerPortNo)+' '+str(self.peerid)


    def getpeerid(self):
        return self.peerid

    def getpeer_port_num(self):
        return self.peerPortNo

    def get_peer_host_name(self):
        return self.peerHostname


   
# method to handle peers
def handlePeer(data,clientsocket,clientaddr):
    global count
    print "*"*20
    print "Request received from Client :"
    print data
    print "*"*20
    rlist=shlex.split(data)
    # considering variours inputs and performing actions accordingly
    if rlist[0] == 'REGISTER':
        count=add_peer_to_list(data)
        reply="Thank you for registering"
        clientsocket.send(reply)
    elif rlist[0] == 'LISTALL':
        reply,code,phrase=listAll()
        response="P2P-CI/1.0 "+str(code)+" "+str(phrase)+"\n"
        for i in reply:
            reply_list=shlex.split(str(i))
            response=response+str(reply_list[0])+" "+reply_list[1]+" "+reply_list[2]+" "+str(reply_list[3])+"\n"
            
        clientsocket.send(response)
    elif rlist[0] == 'LOOKUP':
        reply,code,phrase=lookup(rlist[1])
        response="P2P-CI/1.0 "+str(code)+" "+str(phrase)+"\n"
        for i in reply:
            reply_list=shlex.split(str(i))
            response=response+str(reply_list[0])+" "+reply_list[1]+" "+reply_list[2]+" "+str(reply_list[3])+"\n"
        clientsocket.send(response)
    elif rlist[0] == 'ADD':
        reply,code,phrase=add_RFC_Index(rlist[1],rlist,count)
        a=data.splitlines()
        title=a[3].split(":")
        response="P2P-CI/1.0 "+str(code)+" "+str(phrase)+"\n"
        response=response+"RFC "+rlist[1]+" "+title[1]+" "+rlist[4]+" "+rlist[6]
        clientsocket.send(response)
    elif rlist[0] == 'EXIT':
        remove_client(rlist,count)
        response="Bye"
        clientsocket.send(response)
    elif rlist[0] == 'REMOVE':
        rfc_remove(rlist[1],rlist,count)
        response="Done - > RFC removed successfully"
        clientsocket.send(response)
        

# method to remove RFC
def rfc_remove(rfc_number,rlist,count):
     rfc_pos = 0
     phostname=rlist[4]
     peerport=rlist[6]
     rfc_title=rlist[8]
     for q in index_list:
        if q.rfc_number==rfc_number and q.peerHostname==phostname:
            del index_list[rfc_pos]
        rfc_pos = rfc_pos + 1
            

# method to remove client
def remove_client(rlist, count):
    global peerhost
    templ=list()
    temil=list()
    phostname=rlist[3]
    peerport=rlist[5]
    for q in peer_list:
        if q.peerPortNo==peerport:
            peerhost=q.peerHostname
            idx2=[x for x,y in enumerate(index_list) if y.peerHostname==str(peerhost)]
            for i in sorted(idx2, reverse=True):
                del index_list[i]
    
    
    idx=[x for x,y in enumerate(peer_list) if y.peerPortNo==peerport]
    for i in idx:
        del peer_list[i]

# method to add peer
def add_peer_to_list(data):
    global count
    count = count+1
    rlist=shlex.split(data)
    temp=list()
    a=list()
    b=list()
    rfc_list=str(data).rsplit(':',1)
    c=shlex.split(rfc_list[1])
    peer_list.insert(0,PeerRecord(rlist[3],rlist[5],count))
    for i,j in zip(c[::2],c[1::2]):
        index_list.insert(0,RFCRecord(i,j,rlist[3],count))
    return count

# method to list all rfcs
def listAll():
    global status
    status=0
    global phrase
    phrase=''

    temp=list()
    if not index_list:
        status=404
        phrase='BAD REQUEST'
    else:
        for x in index_list:
            temp.append(RFCRecord(x.rfc_number,x.rfc_title,x.peerHostname,x.peerid))
            status=200
            phrase='OK'
    return temp,status,phrase


# method to look up for RFC based on rfc number
def lookup(rfc_number):
    temp=list()
    flag=0
    for x in index_list:
        if int(x.rfc_number)==int(rfc_number):
            temp.append(RFCRecord(x.rfc_number,x.rfc_title,x.peerHostname,x.peerid))
            code=200
            phrase='OK'
            flag = 1
        #else:
            #code=404
            #phrase='FILE NOT FOUND'
    if(flag==0):
        code=404
        phrase='FILE NOT FOUND'
    return temp,code,phrase

# method to add RFC index
def add_RFC_Index(rfc_number,rlist,count):
    index_list.insert(0,RFCRecord(rfc_number,rlist[8],rlist[4],count))
    for x in index_list:
        code=200
        phrase='OK'
    return index_list,code,phrase

def check():
	print "Check"
	print "LOOKUP"
	print "ADD RFC"
	print "Remove RFC"
	print "List of active clients"
	print "Download RFC"

# handler method
def handler(clientsocket, clientaddr):
    #print "Accepted connection from: ", clientaddr

    data = clientsocket.recv(1024)
    cur_thread=threading.current_thread()
    handlePeer(data,clientsocket,clientaddr)


    
if __name__=="__main__":
    #HOST='127.0.0.1'
    HOST=socket.gethostname()
    PORT=7734
    print HOST
    serversocket = socket.socket()
    dns_resolved_addr = socket.gethostbyname(HOST)
    serversocket.bind((dns_resolved_addr,PORT))

    serversocket.listen(5)

    print "Server listening for connection requests \n"
    
    while(1):
        

        clientsocket, clientaddr = serversocket.accept()
        # creting server thread
        serverThread = threading.Thread(target=handler, args=(clientsocket,clientaddr))
        serverThread.start()
    # close server socket
    serversocket.close()

    
