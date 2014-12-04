class Observable:
    """Abstract class Observable
    """
    def __init__(self):
        # Attributes:
        self.__observers = []  # (Objects) 
    
    # Operations
    def addObserver(self, observer):
        """function addObserver
        
        observer: any type of object (it musts implement update() )
        """
        if not observer in self.__observers:
            self.__observers.append(observer)
    
    def removeObserver(self, observer):
        """function removeObserver
        
        observer: Object
        """
        try:
            self.__observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, source=None):
        """function notfy
        
        source: any object that initiated a change
        """
        for i in self.__observers:
            if i != source:
                i.update(self,  source)
    

