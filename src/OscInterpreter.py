from Observable import Observable

class OscInterpreter(Observable):
    def __init__(self,  device):
        self.device = device #AbstractDevice
        Observable.__init__(self)
        self.__acceptedAddressPrefixesIn = [] # (string[])
        
    def receiveOscMsg(self,  msg):
        """function receiveOscMsg
        
        msg: OscMsg
        
        returns void
        """
        raise NotImplementedError()
    
    def addAcceptedAddressPrefixIn(self,  acceptedAddressPrefixIn):
        """function addAcceptedAddressPrefixIn
        
        acceptedAddressPrefixIn: string
        
        returns void
        """
        if not acceptedAddressPrefixIn in self.__acceptedAddressPrefixesIn:
            self.__acceptedAddressPrefixesIn.append(acceptedAddressPrefixIn)
            self.notify("acceptedAddressPrefixesIn")
    
    def removeAcceptedAddressPrefixIn(self,  acceptedAddressPrefixIn):
        """function removeAcceptedAddressPrefixIn
        
        acceptedAddressPrefixIn: string
        
        returns void
        """
        try:
            self.__acceptedAddressPrefixesIn.remove(acceptedAddressPrefixIn)
            self.notify("acceptedAddressPrefixesIn")
        except ValueError:
            pass
    
    def isPrefixValid(self, msg):
        """function isPrefixValid

        msg: OscMsg

        returns boolean
        """
        accepted = False

        for i in self.__acceptedAddressPrefixesIn:
            if msg.getOscAddress().startswith(i):
                accepted = True
                break

        return accepted
    
    def findSuffix(self, msg):
        """function findSuffix

        msg: OscMsg

        returns string
        """
        suffix = None
        for i in self.__acceptedAddressPrefixesIn:
            if msg.getOscAddress().startswith(i):
                suffix = msg.getOscAddress()[msg.getOscAddress().find(i)+len(i):]
                break
        return suffix
