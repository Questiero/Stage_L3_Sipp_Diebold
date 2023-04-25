from ..Formula import Formula
from ..unary.Not import Not

class NaryFormula(Formula):
    
    def toDNF(self):
        return self
    
    def toDNFNeg(self):
        return Not(self)