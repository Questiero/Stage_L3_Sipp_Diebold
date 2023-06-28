from __future__ import annotations

from .binaryFormula import BinaryFormula
from ...constants import Constants

# Typing only imports
from .. import Formula

class Equivalence(BinaryFormula):
    '''
     Class representing the biconditional operator.

    Attributes
    ----------
    children: tuple of Formulas
        The children of the current node.
    '''
    
    _symbol = "<->"
    
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the biconditional operator,
        using only Not, And and Or.In this case, it's (a AND b) OR (NOT a AND NOT b).

        Returns
        -------
        formula: Formula
            The simplified version of the biconditional operator. In this case,
            it's (a AND b) OR (NOT a AND NOT b).
        '''
           
        return (self.children[0] & self.children[1]) | (~self.children[0] & ~self.children[1])
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        childrenModified = []
        for child in self.children: childrenModified.append(child.toLessOrEqConstraint())

        return Equivalence(childrenModified[0], childrenModified[1])
    
    def __str__(self):
        return "(" + str(self.children[0]) + ") " + Constants.EQUIVALENCE_STRING_OPERATOR +  " (" + str(self.children[1]) + ")"

    def toLatex(self):
        return "(" + self.children[0].toLatex() + ") " + Constants.EQUIVALENCE_LATEX_OPERATOR +  " (" + self.children[1].toLatex() + ")"
