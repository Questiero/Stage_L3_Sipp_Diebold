import formula
import notOperator

class NullaryFormula(formula.Formula):
        
    def toDNF(self):
        return self
    
    def _toDNFNeg(self):
        return notOperator.Not(self)