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
    hasMsg = False
    msg = ""

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
            if(self.connected and self.hasMsg):
                self.sendMsg(self.msg)

    def connectToServer(self):
        try:
            self.sock.connect((self.address, self.port)) 
            return True
        except Exception as e:
            self.closeSocket() 
            return False

    def sendMsg(self, msg):
        try:                
            if(not self.connected):
                print "ime is not connected"
                return
            self.sock.sendto(msg.encode('utf-8'), (self.address, self.port))
            self.emptyMsgTray()
            if(msg == "CMD::STOP"):
                self.initVars()
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            self.initVars()
            print 'disconnected.'
            return False

    def setMsg(self, msg):
        if(not self.connected):
            return
        self.msg = msg
        self.hasMsg = True

    def initVars(self):
        self.running = True 
        self.connected = False
        self.conTryLabel = False
        self.emptyMsgTray()

    def emptyMsgTray(self):
        self.hasMsg = False
        self.msg = ""        

    def closeSocket(self):
        self.sock.close()
        self.sock = socket.socket()

    def destroy(self):
        if(self.connected):
            self.sendMsg('CMD::STOP');
        self.running = False

