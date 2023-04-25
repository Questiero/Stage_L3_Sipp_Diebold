from ..Formula import Formula
from abc import abstractmethod

class BinaryFormula(Formula):
        
    # formulas: tuple (Formula, Formula)
    def __init__(self, formulaTuple):
        self._children = formulaTuple

    @abstractmethod
    def _simplify(self):
        pass
    
    def getVariables(self):
        return self._children.getVariables()
    
    def toDNF(self):
        return self._simplify().toDNF()
    
    def _toDNFNeg(self):
        return self._simplify()._toDNFNeg()