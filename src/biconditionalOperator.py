import binaryFormula

# Typing only imports
import formula

class Biconditional(binaryFormula.BinaryFormula):
    '''
     Class representing the biconditional operator.

    Attributes
    ----------
    _children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the biconditional syntaxically.
    '''
    
    _symbol = "<=>"
    
    def _simplify(self) -> formula.Formula:
        '''
        Method returning the simplified form for the biconditional operator,
        using only Not, And and Or.In this case, it's (a AND b) OR (NOT a AND NOT b).

        Returns
        -------
        formula: Formula
            The simplified version of the biconditional operator. In this case,
            it's (a AND b) OR (NOT a AND NOT b).
        '''
           
        return (self._children[0] & self._children[1]) | (~self._children[0] * ~self._children[1])