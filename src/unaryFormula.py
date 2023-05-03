import formula

class UnaryFormula(formula.Formula):
            
    # formula: Formula
    def __init__(self, formulaInit):
        self._children = formulaInit
        
    def getVariables(self):
        return self._children.getVariables()
    
    def __str__(self):
        return self._symbol + "(" + self._children + ")"