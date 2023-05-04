import formula

class NaryFormula(formula.Formula):
        
    # formula: Set(Formula)
    def __init__(self, *formulas):
                
        self._children = set(formulas)
                
        if len(self._children) >= 2:
            tempF = set()
            
            for formul in self._children:
                if isinstance(formul, type(self)):
                    tempF.add(formul)
                    self._children = self._children | formul._children
                    
            self._children = self._children - tempF

        else:
            raise Exception("nary operators need at least two formulas")
        
    def getVariables(self):
        tempChildren = self._children.copy()
        variables = tempChildren.pop().getVariables();
        for child in tempChildren:
            variables = variables | child.getVariables()
        return variables
    
    def __str__(self):
        s = "("
        for child in self._children:
            s += str(child) + " " + self._symbol + " "
        toRemove = len(self._symbol) + 2
        s = s[:-toRemove] + ")"
        return s