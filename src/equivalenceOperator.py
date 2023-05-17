from binaryFormula import BinaryFormula

# Typing only imports
from formula import Formula

class Equivalence(BinaryFormula):
    '''
     Class representing the biconditional operator.

    Attributes
    ----------
    children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the biconditional syntaxically.
    '''
    
    _symbol = "<->"
    
    def _simplify(self) -> Formula:
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