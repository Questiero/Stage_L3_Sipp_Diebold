from .NullaryFormula import NullaryFormula

class Top(NullaryFormula):
    
    _symbol = "TOP"
    
    def getVariables(self):
        return None
    
    def getConstraintGonfle(self):
        return []
    
    def getConstraintGonfleNeg(self):
        return []