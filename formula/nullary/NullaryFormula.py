from ..Formula import Formula
from ..unary.Not import Not

class NullaryFormula(Formula):
    
    def toDNF(self):
        return self
    
    def _toDNFNeg(self):
        return Not(self)