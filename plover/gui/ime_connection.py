""" New Class added """

import socket
import sys
import threading


class ImeConnection(threading.Thread):

    sock = socket.socket()
    address = 'localhost'
    port = 12345
    running = True 
    connected = False
    conTryLabel = False

    def __init__(self, mainFrame):
        threading.Thread.__init__(self)
        self.frame = mainFrame

    def run(self):
        self.initVars()
        while(self.running):
            connected_K1 = self.connected
            if(not self.connected):
                if(not self.conTryLabel):
                    print 'connecting to IME...'
                    self.conTryLabel = True
                self.connected = self.connectToServer()
            if(not connected_K1 and self.connected):
                print 'connected.'
                self.conTryLabel = False

    def connectToServer(self):
        try:
            self.sock.connect((self.address, self.port)) 
            return True
        except Exception as e:
            self.closeSocket() 
            return False

    def sendMsg(self, msg):
        try:                
            self.sock.sendto(msg.encode('utf-8'), (self.address, self.port))
            if(message == "CMD::STOP"):
                initVars()
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            self.initVars()
            print 'disconnected.'
            return False

    def initVars(self):
        self.running = True 
        self.connected = False
        self.conTryLabel = False

    def closeSocket(self):
        self.sock.close()
        self.sock = socket.socket()

    def destroy(self):
        if(self.connected):
            self.sendMsg('CMD::STOP');
        self.running = False
