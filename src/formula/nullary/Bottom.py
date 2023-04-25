from .NullaryFormula import NullaryFormula

class Bottom(NullaryFormula):
    
    symbol = "BOT"
    
    def getVariables(self):
        return None