import binaryFormula

# Typing only imports
import formula

class Xor(binaryFormula.BinaryFormula):
    '''
     Class representing the XOR operator.

    Attributes
    ----------
    _children: tuple of Formulas
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
        return (self._children[0] * -self._children[1]) + (-self._children[0] * self._children[1])