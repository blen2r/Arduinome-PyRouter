from OscDevice import OscDevice
from SerialDevice import SerialDevice

import threading
import time

class AbstractDevice(threading.Thread, OscDevice,  SerialDevice):
    def __init__(self,  serialNumber,  baudrate,  device):
        threading.Thread.__init__(self)
        SerialDevice.__init__(self, serialNumber,  baudrate,  device)
        OscDevice.__init__(self)
        self.__active = False
    
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
        else:
            self._SerialDevice__connection.flush()
        self.notify("active")
    
    def run(self):
        """function run
        checks for serial messages
        
        returns void
        """
        while self.__active:
            if self._SerialDevice__connection.inWaiting():
                msg = self.readMsg(self.getMessageSize())
                self.handleSerialDeviceMessageReceivedEvent(msg)
                time.sleep(0.001)
            else:
                time.sleep(0.001)
    
    def handleSerialDeviceMessageReceivedEvent(self, msg):
        """function handleSerialDeviceMessageReceivedEvent
        handles serial messages
        
        returns void
        """
        raise NotImplementedError()
