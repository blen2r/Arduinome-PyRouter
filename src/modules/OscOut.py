#import 1
from Observable import Observable
from AbstractModule import AbstractModule

import threading
import socket

class OscOut(Observable, AbstractModule):
    """Class OscOut
    """
    def __init__(self, oscAddressPatternPrefix,  hostAddress="127.0.0.1",  hostPort=8000):
        AbstractModule.__init__(self)
        Observable.__init__(self)
        # Attributes:
        self.setOscAddressPatternPrefix(oscAddressPatternPrefix)  # (string)
        if self.__oscAddressPatternPrefix.endswith("/"):
            self.setOscAddressPatternPrefix(self.__oscAddressPatternPrefix[:-1])
        self.setHostAddress(hostAddress)  # (string) 
        self.setHostPort(hostPort)  # (int) 
        self.__msgBuffer = [] # (OscMsg[])
        self.__outSocket = None#socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__active = False
        
        #runnables for the CLI
        self.runnables.append("getActive()")
        self.runnables.append("setActive(bool active)")
        self.runnables.append("getHostAddress()")
        self.runnables.append("setHostAddress(string hostAddress)")
        self.runnables.append("getHostPort()")
        self.runnables.append("setHostPort(int hostPort)")
        self.runnables.append("getOscAddressPatternPrefix()")
        self.runnables.append("setOscAddressPatternPrefix(string oscAddressPatternPrefix)")
        
    
    def setOscAddressPatternPrefix(self, oscAddressPatternPrefix):
        """function setOscAddressPatternPrefix
        
        oscAddressPatternPrefix: string
        
        returns void
        """
        self.__oscAddressPatternPrefix = oscAddressPatternPrefix
        self.notify("oscAddressPatternPrefix")
    
    def getOscAddressPatternPrefix(self):
        """function getOscAddressPatternPrefix
        
        returns string
        """
        return self.__oscAddressPatternPrefix
    
    def setHostPort(self, hostPort):
        """function setHostPort
        
        hostPort: int
        
        returns void
        """
        self.__hostPort = hostPort
        self.notify("hostPort")
    
    def getHostPort(self):
        """function getHostPort
        
        returns int
        """
        return self.__hostPort
    
    def setHostAddress(self, hostAddress):
        """function setHostAddress
        
        hostAddress: string
        
        returns void
        """
        self.__hostAddress = hostAddress
        self.notify("hostAddress")
    
    def getHostAddress(self):
        """function getHostAddress
        
        returns string
        """
        return self.__hostAddress
    
    def addOscMsg(self, msg):
        """function addOscMsg
        
        msg: OscMsg
        
        returns void
        """
        if self.__active:
            self.__outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #print "debug MonomeOscOut: ",  self.__oscAddressPatternPrefix + msg.getOscAddress(),  msg.getTypeTags(),  msg.getData()
            
            self.__outSocket.sendto(msg.toBinary(self.__oscAddressPatternPrefix + msg.getOscAddress()),  (self.__hostAddress,  self.__hostPort)) #inspired by simpleOSC's API. 
            self.__outSocket.close()
    
    def getActive(self):
        """function getActive
        
        returns boolean
        """
        return self.__active
    
    def setActive(self,  active):
        """function setActive
        
        active: boolean
        
        returns void
        """
        self.__active = active
        
        self.notify("active")

