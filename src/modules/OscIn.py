#import 1
from OscMsg import OscMsg
from Observable import Observable
from AbstractModule import AbstractModule

import threading
import socket
import string
import struct
import math

############################### simpleOSC' functions to decode OSC messages
## I needed to copy those functions because the way simpleOSC handles sockets wasn't compatible with this project
def readString(data):
    length   = string.find(data,"\0")
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length], data[nextData:])
        
def readBlob(data):
    length   = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])

def readInt(data):
    if(len(data)<4):
        print "Error: too few bytes for int", data, len(data)
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]

    return (integer, rest)

def readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high, low = struct.unpack(">ll", data[0:8])
    big = (long(high) << 32) + low
    rest = data[8:]
    return (big, rest)

def readDouble(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit double float."""
    floater = struct.unpack(">d", data[0:8])
    big = float(floater[0])
    rest = data[8:]
    return (big, rest)

def readFloat(data):
    if(len(data)<4):
        print "Error: too few bytes for float", data, len(data)
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (float, rest)
###############################

class OscIn(threading.Thread, Observable, AbstractModule):
    """Class OscIn
    """
    def __init__(self, listenAddress="127.0.0.1", listenPort=8080):
        AbstractModule.__init__(self)
        threading.Thread.__init__(self)
        Observable.__init__(self)
        # Attributes:
        self.__oscInterpreters = []  # (OscInterpreter) 
        self.setListenAddress(listenAddress)  # (string) 
        self.setListenPort(listenPort)  # (int) 
        self.__inSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__inSocket.settimeout(10)
        self.__active = False
        
        #runnables for the CLI
        self.runnables.append("getActive()")
        self.runnables.append("setActive(bool active)")
        self.runnables.append("getListenPort()")
        self.runnables.append("setListenPort(int listenPort)")
        self.runnables.append("getListenAddress()")
        self.runnables.append("setListenAddress(string listenAddress)")
        self.runnables.append("addOscInterpreter(OscInterpreter obj)")
        self.runnables.append("removeOscInterpreter(OscInterpreter obj)")
        
        
    
    # Operations
    def run(self):
        """function run

        returns void
        """
        try :
            self.__inSocket.bind( (self.__listenAddress, self.__listenPort) )
        except socket.error :
            print "Error: could not open the socket for input!"
            
        while self.__active: #inspired by the simpleOSC's API
            try:
                data = self.__inSocket.recv(1024)
                #print "debug data received: ", data
                if data is not None:
                    self.receiveData( data )
            except socket.timeout:
                pass
                
        self.__inSocket.close()
    
    def getListenAddress(self):
        """function getListenAddress
        
        returns string
        """
        return self.__listenAddress
    
    def setListenAddress(self, listenAddress):
        """function setListenAddress
        
        listenAddress: string
        
        returns void
        """
        self.__listenAddress = listenAddress
        self.notify("listenAddress")

    def getListenPort(self):
        """function getListenPort
        
        returns int
        """
        return self.__listenPort
    
    def setListenPort(self, listenPort):
        """function setListenPort
        
        listenPort: int
        
        returns void
        """
        self.__listenPort = listenPort
        self.notify("listenPort")
    
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
        
        if active and not self.isAlive():
            self.start()
            
        self.notify("active")
    
    def addOscInterpreter(self,  interpreter):
        """function addOscInterpreter
        
        interpreter: OscInterpreter
        
        returns void
        """
        if not interpreter in self.__oscInterpreters:
            self.__oscInterpreters.append(interpreter)
    
    def removeOscInterpreter(self,  interpreter):
        """function removeDevice
        
        device: MonomeXXhDevice
        
        returns void
        """
        try:
            self.__oscInterpreters.remove(interpreter)
        except ValueError:
            pass
    
    def decodeOSC(self,  data): #shamelessly stolen from simpleOSC's API
        """Converts a typetagged OSC message to a Python list."""
        table = { "i" : readInt, "f" : readFloat, "s" : readString, "b" : readBlob, "d" : readDouble }
        decoded = []
        address,  rest = readString(data)
        typetags = ""

        if address == "#bundle":
            time, rest = readLong(rest)
    #       decoded.append(address)
    #       decoded.append(time)
            while len(rest)>0:
                length, rest = readInt(rest)
                decoded.append(decodeOSC(rest[:length]))
                rest = rest[length:]

        elif len(rest) > 0:
            typetags, rest = readString(rest)
            decoded.append(address)
            decoded.append(typetags)
            if typetags[0] == ",":
                for tag in typetags[1:]:
                    value, rest = table[tag](rest)
                    decoded.append(value)
            else:
                print "Oops, typetag lacks the magic ,"

        return decoded
    
    def receiveData(self,  data):
        """function receiveData
        
        data: string
        
        returns void
        """
        #print  "debug data received OscIn: ",  data
        
        decoded = self.decodeOSC(data) #from simpleOSC's API
        #print "debug decoded: ",  decoded
        
        #convert from format ["address", ",iii", 100, 101, 102] to format ["address", "iii", [100,101,102]]
        msg = []
        msg.append(decoded[0])
        if decoded[1].startswith(","):
            msg.append(decoded[1][1:])
        else:
            msg.append(decoded[1])
        msg.append(decoded[2:])
        
        self.dispatch(msg)
    
    def dispatch(self, message):
        #modified version of simpleOSC's API' callback manager version 0.2.7, file OSC.py, line 268)
        #print "debug dispatch: ",  message
        
        try:
            if type(message[0]) == str :
                # got a single message
                address = message[0]
                typeTags = message[1]
                data = message[2]
                #this line was changed from simpleOSC's API
                msg = OscMsg(address,  typeTags, data)
                #print "debug in: ",  msg.getOscAddress(),  msg.getTypeTags(),  msg.getData()
                
                for interpreter in self.__oscInterpreters:
                    interpreter.receiveOscMsg(msg)

            elif type(message[0]) == list :
                # smells like nested messages
                for msg in message :
                    self.dispatch(msg, source)

        except KeyError, e:
            # address not found
            print 'address %s not found ' % address
            pprint.pprint(message)
        except IndexError, e:
            print 'got malformed OSC message'
            pass
        except None, e:
            print "Exception in", address, "callback :", e


