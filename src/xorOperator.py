import binaryFormula

# Typing only imports
import formula

class Xor(binaryFormula.BinaryFormula):
    '''
     Class representing the XOR operator.

    Attributes
    ----------
    children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the XOR syntaxically.
    '''
    
    _symbol = "XOR"
    
    def _simplify(self) -> formula.Formula:
        '''
        Method returning the simplified form for the XOR operator, using only
        Not, And and Or.In this case, it's (a AND NOT b) OR (NOT a AND b).

        Returns
        -------
        formula: Formula
            The simplified version of the implication operator. In this case, it's
            (a AND NOT b) OR (NOT a AND b).
        '''
        return (self.children[0] & ~self.children[1]) | (~self.children[0] & self.children[1])
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        childrenModified = []
        for child in self.children: childrenModified.append(child.toLessOrEqConstraint())

        return Xor(childrenModified[0], childrenModified[1])