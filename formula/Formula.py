from abc import ABC, abstractmethod

class Formula(ABC):
    
    _children = None
    _symbol = ""
    
    @abstractmethod
    def getVariables(self):
        pass
    
    @abstractmethod
    def toDNF(self):
        pass
    
    @abstractmethod
    def _toDNFNeg(self):
        pass