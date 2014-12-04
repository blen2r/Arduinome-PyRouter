from Message import Message
from Observable import Observable

import serial

class SerialDevice(Observable):
    """Abstract class SerialDevice
    """
    def __init__(self, serialNumber, baudRate, device):
        Observable.__init__(self)
        # Attributes:
        self.setSerialNumber(serialNumber)  # (string) 
        self.__device = device
        self.__bytesize = serial.EIGHTBITS
        self.__parity = serial.PARITY_NONE
        self.__stopbits = serial.STOPBITS_ONE
        self.__xonxoff = 0
        self.__connection = None
        self.__messageSize = None
        
        #we set the baud rate depending on the type of microcontroller
        self.__baudrate = baudRate
        
        #we open the connection
        try:
            self.__connection = serial.Serial(port=self.__device,  baudrate=self.__baudrate,  bytesize=self.__bytesize,  parity=self.__parity,  stopbits=self.__stopbits,  xonxoff=self.__xonxoff)
        except serial.SerialException:
            print "Unable to connect to the device!"
    
    def __del__(self):
        #we must close the connection before the object is destroyed
        if self.__connection is not None:
            self.__connection.flush()
            self.__connection.close()
    
    def setSerialNumber(self, serialNumber): 
        """function setSerialNumber
        
        serialNumber: string
        """
        self.__serialNumber = serialNumber
        self.notify("serialNumber")
    
    def write(self, data):
        """function write
        This method sends data to the device
        
        data: byte
        
        returns void
        """
        self.__connection.write(chr(data))
    
    def read(self):
        """function read
        This method receives data from the device, 1 byte
        You should use readMsg instead of this method
        
        returns byte read
        """
        data = ord(self.__connection.read(1))
        print "debug read: ",  data
        return data
    
    def getSerialNumber(self): 
        """function getSerialNumber
        
        returns string
        """
        return self.__serialNumber
    
    def getMessageSize(self):
        """function getMessageSize

        returns int
        """
        return self.__messageSize
    
    def setMessageSize(self,  messageSize):
        """function setMessageSize

        messageSize: int

        returns void
        """
        self.__messageSize = messageSize
    
    def writeMsg(self, message):
        """function writeMsg
        
        message: Message
        
        returns void
        """
        #print "debug serial writeMsg: ",  id(message),  message.data
        for i in message.data:
            self.write(i)
#        self.write(message.data[0])
#        self.write(message.data[1])
    
    def readMsg(self,  nBytes):
        """function readMsg
        
        nBytes: int (number of bytes to read)
        
        returns Message
        """
        msg = Message()
        for i in range(nBytes):
            msg.data.append(self.read())
        #print "debug readMsg: ",  msg.data
        return msg
    
    

