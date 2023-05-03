from ..formula import Formula
from ..unary.notOperator import Not

class NullaryFormula(Formula):
        
    def toDNF(self):
        return self
    
    def _toDNFNeg(self):
        return Not(self)