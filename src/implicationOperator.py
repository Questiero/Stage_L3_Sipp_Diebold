from .binaryFormula import BinaryFormula

# Typing only imports
from .formula import Formula

class Implication(BinaryFormula):
    '''
     Class representing the implication operator.

    Attributes
    ----------
    children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the implication syntaxically.
    '''
    
    _symbol = "->"
    
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the implication operator, using only
        Not, And and Or.In this case, it's NOT a OR b

        Returns
        -------
        formula: Formula
            The simplified version of the implication operator. In this case, it's
            NOT a OR b.
        '''
        
        return ~self.children[0] | self.children[1]
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        childrenModified = []
        for child in self.children: childrenModified.append(child.toLessOrEqConstraint())

        return Implication(childrenModified[0], childrenModified[1])