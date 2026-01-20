from abc import ABC, abstractmethod

class State(ABC):
    
    def __init__(self,objRef,stateName):
        self.stateName=stateName
        self.objRef=objRef
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self,group,dt):
        pass
    
    @abstractmethod
    def quit(self):
        pass