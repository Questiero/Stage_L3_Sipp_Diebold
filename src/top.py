import nullaryFormula

class Top(nullaryFormula.NullaryFormula):
    
    _symbol = "TOP"
    
    def getVariables(self):
        return None
    
    def getConstraintGonfle(self):
        return []
    
    def getConstraintGonfleNeg(self):
        return []
    
    def __str__(self):
        return self._symbol;