import formula

# Typing only imports
import variable

class UnaryFormula(formula.Formula):
    '''
    Abstract class, representing a unary operator.

    Attributes
    ----------
    _children: Formula
        The child of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''

    # formula: Formula
    def __init__(self, formulaInit: formula.Formula):
        self._children = formulaInit
        
    def getVariables(self) -> set[variable.Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self._children.getVariables()
    
    def __str__(self):
        return self._symbol + str(self._children)