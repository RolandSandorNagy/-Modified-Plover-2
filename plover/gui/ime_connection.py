""" New Class added """

import socket
import sys
import threading


class ImeConnection(threading.Thread):

    sock = socket.socket()
    host = 'localhost'
    port = 12345
    running = True 
    connected = False
    isActive = False
    conTryLabel = False
    hasMessage = False
    message = ""
    hasSuggestions = False
    suggestions = []

 
    def __init__(self, mainFrame):
        threading.Thread.__init__(self)
        self.frame = mainFrame
        self.host = mainFrame.config.get_ime_host()
        self.port = mainFrame.config.get_ime_port()

    def run(self):
        self.initVars()
        while(self.running):
            connected_K1 = self.connected
            if(not self.connected):
                if(not self.conTryLabel):
                    self.conTryLabel = True
                self.connected = self.connectToServer()
            if(not connected_K1 and self.connected):
                self.frame.updateImeStatus(self.frame.IME_IS_CONNECTED)                
                self.isActive = True
                self.conTryLabel = False
            if(self.connected and self.hasMessage):
                self.sendMessage(self.message)
            if(self.connected and self.hasSuggestions):
                self.sendSuggestions(self.suggestions)

    def connectToServer(self):
        try:
            self.sock.connect((self.host, self.port)) 
            return True
        except Exception as e:
            self.closeSocket() 
            return False

    def sendMessage(self, msg):
        try:                
            if(not self.connected):
                return
            self.sock.sendto(msg.encode('utf-8'), (self.host, self.port))
            self.emptyMsgTray()
            if(msg == self.frame.IME_CMD_STOP):
                self.frame.updateImeStatus(self.frame.IME_IS_DISCONNECTED)
                self.initVars()
            elif(msg == self.frame.IME_CMD_PAUSE):
                self.frame.updateImeStatus(self.frame.IME_IS_PAUSED)
                self.isActive = False
            elif(msg == self.frame.IME_CMD_RESUME):
                self.frame.updateImeStatus(self.frame.IME_IS_CONNECTED)                
                self.isActive = True
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            self.initVars()
            return False

    def setMsg(self, msg):
        if(not self.connected or (not self.isActive and msg != self.frame.IME_CMD_RESUME)):
            return
        self.message = msg
        self.hasMessage = True

    def initVars(self):
        self.running = True 
        self.connected = False
        self.isActive = False
        self.conTryLabel = False
        self.emptyMsgTray()
        self.emptySuggsTray()

    def emptyMsgTray(self):
        self.hasMessage = False
        self.message = ""        

    def emptySuggsTray(self):
        self.hasSuggestions = False
        self.suggestions = []

    def closeSocket(self):
        self.sock.close()
        self.sock = socket.socket()

    def destroy(self):
        if(self.connected):
            self.sendMessage(self.frame.IME_CMD_STOP);
        self.running = False

    def setSuggestions(self, suggs):
        if(not self.connected or not self.isActive):
            return
        self.suggestions = suggs
        self.hasSuggestions = True

    def sendSuggestions(self, suggs):
        # TODO
        print "sending: "
        print suggs
        self.emptySuggsTray()
        return
