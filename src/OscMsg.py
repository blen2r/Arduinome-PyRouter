import osc

class OscMsg:
    """Class OscMsg
    """
    def __init__(self, oscAddress, typeTags, data):
        # Attributes:
        self.__oscAddress = oscAddress  # (string) 
        self.__typeTags = typeTags # (string)
        self.__data = data  # (any_type[]) 
    
    # Operations
    def getOscAddress(self):
        """function getOscAddress
        
        returns string
        """
        address = self.__oscAddress
        if self.__oscAddress.endswith("/"):
            address = self.__oscAddress[:-1]
        
        return address
    
    def getData(self):
        """function getData
        
        returns any_type[]
        """
        return self.__data
    
    def getTypeTags(self):
        """function getTypeTags
        
        returns string[]
        """
        return self.__typeTags
    
    def toBinary(self,  oscAddress):
        """function toBinary
        
        returns binary message
        """
        return osc.createBinaryMsg(oscAddress, self.__data)
    
    def typeTagsMatch(self,  goodTags):
        """function typeTagsMatch
    
        goodTags: string[]
        
        returns boolean
        """
        if len(self.__typeTags) < len(goodTags):
            return False
        
        for i in range(len(goodTags)):
            if self.__typeTags[i] != goodTags[i]:
                return False
        
        return True

