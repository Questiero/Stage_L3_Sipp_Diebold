import nullaryFormula

class Bottom(nullaryFormula.NullaryFormula):
    
    symbol = "BOT"
    
    def getVariables(self):
        return None
    
    def getConstraintGonfle(self):
        return []
    
    def getConstraintGonfleNeg(self):
        return []
    
    def __str__(self):
        return self._symbol;