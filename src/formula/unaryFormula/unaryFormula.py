from __future__ import annotations

from .. import Formula
from ..formulaManager import FormulaManager

# Typing only imports
from ...variable.variable import Variable

class UnaryFormula(Formula):
    '''
    Abstract class, representing a unary operator.

    Attributes
    ----------
    children: Formula
        The child of the current node.
    '''

    # formula: Formula
    def __init__(self, formulaInit: Formula, name: str = None):
        
        self.children = formulaInit

        if(name is not None):
            FormulaManager.declare(name, self)
        
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