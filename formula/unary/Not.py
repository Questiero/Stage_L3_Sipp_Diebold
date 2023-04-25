from .UnaryFormula import UnaryFormula

class Not(UnaryFormula):
    
    _symbol = "!"
    
    def getVariables(self):
        return self._children.getVariables()
    
    def toDNF(self):
        return self._children._toDNFNeg()
    
    def _toDNFNeg(self):
        return self._children.toDNF()