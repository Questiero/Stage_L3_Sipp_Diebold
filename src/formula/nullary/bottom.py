from .NullaryFormula import NullaryFormula

class Bottom(NullaryFormula):
    
    symbol = "BOT"
    
    def getVariables(self):
        return None
    
    def getConstraintGonfle(self):
        return []
    
    def getConstraintGonfleNeg(self):
        return []