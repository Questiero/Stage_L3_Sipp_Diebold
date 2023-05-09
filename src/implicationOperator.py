import binaryFormula

# Typing only imports
import formula

class Implication(binaryFormula.BinaryFormula):
    '''
     Class representing the implication operator.

    Attributes
    ----------
    _children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the implication syntaxically.
    '''
    
    _symbol = "=>"
    
    def _simplify(self) -> formula.Formula:
        '''
        Method returning the simplified form for the implication operator, using only
        Not, And and Or.In this case, it's NOT a OR b

        Returns
        -------
        formula: Formula
            The simplified version of the implication operator. In this case, it's
            NOT a OR b.
        '''
        
        return ~self._children[0] | self._children[1]