from abc import ABC, abstractmethod

class Formula(ABC):
    
    _children = None
    
    @property
    @abstractmethod
    def _symbol(self):
        pass
    
    @abstractmethod
    def getVariables(self):
        pass
    
    @abstractmethod
    def toDNF(self):
        pass
    
    @abstractmethod
    def _toDNFNeg(self):
        pass