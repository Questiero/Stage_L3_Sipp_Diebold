import formula

class NaryFormula(formula.Formula):
        
    # formula: Set(Formula)
    def __init__(self, formulaSet):
        self._children = formulaSet
        
    def getVariables(self):
        tempChildren = self._children.copy()
        variables = tempChildren.pop().getVariables();
        for child in tempChildren:
            variables = variables | child.getVariables()
        return variables