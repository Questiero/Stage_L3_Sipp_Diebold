from .NullaryFormula import NullaryFormula

class Top(NullaryFormula):
    
    _symbol = "TOP"
    
    def getVariables(self):
        return None