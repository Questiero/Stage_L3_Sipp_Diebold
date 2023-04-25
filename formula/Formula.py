from abc import ABC, abstractmethod

class Formula(ABC):
    
    _children = None
    _symbol = ""
    
    @abstractmethod
    def getVariables():
        pass
    
    @abstractmethod
    def toDNF():
        pass
    
    @abstractmethod
    def _toDNFNeg():
        pass