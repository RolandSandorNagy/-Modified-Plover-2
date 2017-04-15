import socket
import sys
import threading


class ImeConnection(threading.Thread):

    sock = socket.socket()
    address = 'localhost'
    port = 12345
    running = True 
    connected = False
    contry = True
    hasMsgToSend = False
    msg = ''

    def __init__(self, mainFrame):
        threading.Thread.__init__(self)
        self.frame = mainFrame

    def run(self):
        while(self.running):
            con = self.connected
            if(not self.connected):
                if(self.contry):
                    print 'connecting...'
                    self.contry = False
                self.connected = self.connectToServer()
            if(not con and self.connected):
                print 'connected.'
                self.contry = True
            if(self.connected and self.hasMsgToSend):
                if(self.sendMsg(self.msg)):
                    self.msg = ''
                    self.hasMsgToSend = False

    def connectToServer(self):
        try:
            self.sock.connect((self.address, self.port)) 
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            return False

    def sendMsg(self, msg):
        try:                
            self.sock.sendto(msg.encode('utf-8'), (self.address, self.port))
            return True
        except Exception as e: 
            self.sock.close()
            self.sock = socket.socket()
            self.connected = False
            print 'disconnected.'
            return False

    def closeConnection(self):
        self.running = False

    def setMsg(self, message):
        self.msg = message
    
    def setHasMsg(self):
        self.hasMsgToSend = True

