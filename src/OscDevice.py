from Observable import Observable

class OscDevice(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.__oscInterpreter = None
        self.__oscOut = [] # (MonomeOscOut)
    
    def setOscInterpreter(self, oscInterpreter):
        """function setOscInterpreter
        
        oscInterpreter: OscInterpreter
        
        returns void
        """
        self.__oscInterpreter = oscInterpreter
    
    def getOscInterpreter(self):
        """function getOscInterpreter
        
        returns OscInterpreter
        """
        return self.__oscInterpreter
    
    def sendMsgToOscOuts(self,  msg):
        """function removeOscOut
        
        msg: OscMsg
        
        returns void
        """
        for i in self.__oscOut:
            i.addOscMsg(msg)
    
    def addOscOut(self,  oscOut):
        """function addOscOut
        
        oscOut: MonomeOscOut
        
        returns void
        """
        if not oscOut in self.__oscOut:
            self.__oscOut.append(oscOut)
    
    def removeOscOut(self,  oscOut):
        """function removeOscOut
        
        oscOut: MonomeOscOut
        
        returns void
        """
        try:
            self.__oscOut.remove(oscOut)
        except ValueError:
            pass
