from ..formula import Formula

class UnaryFormula(Formula):
            
    # formula: Formula
    def __init__(self, formula):
        self._children = formula
        
    def getVariables(self):
        return self._children.getVariables()