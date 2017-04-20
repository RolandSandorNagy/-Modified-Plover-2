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
    isActive = False
    conTryLabel = False
    hasMsg = False
    msg = ""

    IME_IS_CONNECTED = 2
    IME_IS_PAUSED = 1
    IME_IS_DISCONNECTED = 0

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
                self.frame.updateImeStatus(self.IME_IS_CONNECTED)                
                self.isActive = True
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
                self.frame.updateImeStatus(self.IME_IS_DISCONNECTED)
                self.initVars()
            elif(msg == "CMD::PAUSE"):
                self.frame.updateImeStatus(self.IME_IS_PAUSED)
                self.isActive = False
            elif(msg == "CMD::RESUME"):
                self.frame.updateImeStatus(self.IME_IS_CONNECTED)                
                self.isActive = True
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            self.initVars()
            print 'disconnected.'
            return False

    def setMsg(self, msg):
        if(not self.connected or (not self.isActive and msg != "CMD::RESUME")):
            return
        self.msg = msg
        self.hasMsg = True
        print "msg is set"

    def initVars(self):
        self.running = True 
        self.connected = False
        self.isActive = False
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

