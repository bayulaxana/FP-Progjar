import socket
import time
import sys
import asyncore
import logging
from http_server import HttpServer

webServer = HttpServer()
receives = ''

class ClientProcessor( asyncore.dispatcher_with_send ):
    def handle_read(self):
        global receives
        data = self.recv(1024)
        if data:
            d = data.decode()
            receives = receives + d
            
            if receives[-2:] == '\r\n':
                result = webServer.process( receives )
                result = result + '\r\n\r\n'.encode()
                self.send(result)
                receives = ''
                self.close()
        
        self.close()

class Server( asyncore.dispatcher ):
    # constructor
    def __init__(self, portNumber):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind( ('', portNumber) )
        self.listen(5)
        self.portNum = portNumber
        print("New worker running on port {}".format(portNumber))

    def handle_accept(self):
        tup = self.accept()
        if tup is not None:
            sock, addr = tup
            print('[...Worker {} => Connection from {}...]'.format( self.portNum, repr(addr) ))
            handler = ClientProcessor(sock)
    
    def handle_close(self):
        try:
            self.close()
        except:
            pass

def main():
    portNum = 8887
    
    # get the port number via args
    try:
        portNum = int(sys.argv[1])
    except:
        pass

    svr = Server(portNum)
    asyncore.loop()

if __name__ == "__main__":
    main()