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

    @abstractmethod
    def getConstraintGonfle(self):
        pass

    @abstractmethod
    def getConstraintGonfleNeg(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    def __add__(self, a):
        import orOperator
        return orOperator.Or(self, a)    
    
    def __mul__(self, a):
        import andOperator
        return andOperator.And(self, a)
    
    def __neg__(self):
        import notOperator
        return notOperator.Not(self)    