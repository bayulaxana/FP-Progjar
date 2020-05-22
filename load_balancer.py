import socket
import time
import sys
import asyncore
import logging
from asynchronous_server import Server

# initial server dan worker adalah list initial
# penambahan worker terjadi pada extended worker dan server
# semangat bermain-main
# kodingan sebisa mungkin aku buat understandable

# pake format camelCase ya ntar penamaan variabel, fungsinya, class

class BackendList:
    # constructor
    def __init__(self):
        # lists of servers (address, port) and workers
        self.initialServers = [
            ('127.0.0.1', 8887)
        ]
        self.extendedServers = []
        self.initialWorkers  = []
        self.extendedWorkers = []
        
        # counter and port tracker
        self.currCount = 0
        self.currentPort = 8887

        # initiate initial workers (8887)
        for server in self.initialServers:
            portNum = server[1]
            srv = Server(portNum)
            self.initialWorkers.append(srv)
    
    def disconnectWorkers(self, index: int):
        # close the extended workers connection
        for worker in self.extendedWorkers:
            worker.close()
        # pop all server from extended server list
        for n in self.extendedServers:
            self.extendedServers.pop()
        
        # reset the state
        self.currCount = 0
        self.currentPort = 8887

    def getServer(self):
        if self.currCount >= len(self.initialServers):
            self.currCount += 1
            self.currentPort += 1
            serv = ('127.0.0.1', self.currentPort)
            newWorker = Server(self.currentPort)
            
            self.extendedServers.append(serv)
            self.extendedWorkers.append(newWorker)
            return serv
        else:
            serv = self.initialServers[ self.currCount ]
            self.currCount += 1
            return serv

# instance of backend list
# set globally
backendServers = BackendList()

class Backend( asyncore.dispatcher_with_send ):
    # constructor
    def __init__(self, targetAddress):
        asyncore.dispatcher_with_send.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(targetAddress)
        self.portNum = targetAddress[1]
        self.connection = self
    
    def handle_read(self):
        try:
            self.client_socket.send( self.recv(8192) )
        except:
            pass
    
    def handle_close(self):
        try:
            self.close()
            self.client_socket.close()
        except:
            pass

class ClientProcessor( asyncore.dispatcher ):    
    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.backend.client_socket = self
            self.backend.send(data)

    def handle_close(self):
        self.close()

class ServerLoadBalancer( asyncore.dispatcher ):
    # constructor
    def __init__(self, portNumber):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind( ('', portNumber) )
        self.listen(5)
        print("Load Balancer running on port {}".format(portNumber))
        print("=======================================\n")
    
    def handle_accept(self):
        tup = self.accept()
        if tup is not None:
            sock, addr = tup
            print('Incoming connection from {}'.format( repr(addr) ))

            # load balancing here
            balanceServer = backendServers.getServer()
            print("\tConnection from {} redirected to {}".format(addr, balanceServer))
            backend = Backend(balanceServer)

            # get the handler
            handler = ClientProcessor(sock)
            handler.backend = backend

if __name__ == "__main__":
    portNumber = 45100

    # get the port number via args
    try:
        portNumber = int(sys.argv[1])
    except:
        pass

    serv = ServerLoadBalancer(portNumber)
    asyncore.loop()