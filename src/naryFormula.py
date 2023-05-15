import formula

# Typing only imports
import variable

class NaryFormula(formula.Formula):
    '''
    Abstract class, representing an operator with an arity equal or greater
    than 2 in PCMLC as a syntax tree.
    The operator is asummed symmetric.

    Parameters
    ----------
    *formulas: Formula
        The formulas meant as components of the n-ary operator.

    Attributes
    ----------
    children: set(Formula)
        The children of the current node.
    _symbol: str
        The symbol used to represent the operator syntaxically.
    '''
        
    def __init__(self, *formulas: formula.Formula, formulaSet: set[formula.Formula]=None):
        
        if formulaSet is None:
            self.children = set(formulas)
        else:
            self.children= formulaSet
                
        if len(self.children) >= 2:
            tempF = set()
            
            for formul in self.children:
                if isinstance(formul, type(self)):
                    tempF.add(formul)
                    self.children = self.children | formul.children
                    
            self.children = self.children - tempF

        else:
            raise Exception("nary operators need at least two formulas")
        
    def getVariables(self) -> set[variable.Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the n-ary Formula's children.

        Returns
        -------
        variables: set of Variable
            All the variables used in the n-ary Formula or its children.
        '''
        
        tempChildren = self.children.copy()
        variables = tempChildren.pop().getVariables();
        
        for child in tempChildren:
            variables = variables | child.getVariables()
            
        return variables
    
    def __str__(self):
        s = "("
        for child in self.children:
            s += str(child) + " " + self._symbol + " "
        toRemove = len(self._symbol) + 2
        s = s[:-toRemove] + ")"
        return s