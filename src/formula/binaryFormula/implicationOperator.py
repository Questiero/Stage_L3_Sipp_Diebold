"""
Class representing the implication operator.
"""

from __future__ import annotations

from .binaryFormula import BinaryFormula
from ...constants import Constants

# Typing only imports
from .. import Formula

class Implication(BinaryFormula):
    '''
     Class representing the implication operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the implication operator.

    Attributes
    ----------
    children: tuple of src.formula.formula.Formula
        The children of the current node.
    '''
    
    _symbol = "->"
    
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the implication operator, using only
        Not, And and Or.
        In this case, it's NOT a OR b.

        Returns
        -------
        src.formula.formula.Formula
            The simplified version of the implication operator.
            In this case, it's NOT a OR b.
        '''
        
        return ~self.children[0] | self.children[1]
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `src.formula.formula.Formula` into another one, with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        childrenModified = []
        for child in self.children: childrenModified.append(child.toLessOrEqConstraint())

        return Implication(childrenModified[0], childrenModified[1])
    
    def __str__(self):
        return "(" + str(self.children[0]) + ") " + Constants.IMPLICATION_STRING_OPERATOR +  " (" + str(self.children[1]) + ")"

    def toLatex(self):
        return "(" + self.children[0].toLatex() + ") " + Constants.IMPLICATION_LATEX_OPERATOR +  " (" + self.children[1].toLatex() + ")"
