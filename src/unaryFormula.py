from .formula import Formula

# Typing only imports
from .variable import Variable

class UnaryFormula(Formula):
    '''
    Abstract class, representing a unary operator.

    Attributes
    ----------
    children: Formula
        The child of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''

    # formula: Formula
    def __init__(self, formulaInit: Formula):
        self.children = formulaInit
        
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self.children.getVariables()
    
    def __hash__(self):
        return hash(self.children)
    
    def __str__(self):
        return self._symbol + "(" + str(self.children) + ")"