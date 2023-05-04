import binaryFormula
import notOperator
import orOperator
import andOperator


class Biconditional(binaryFormula.BinaryFormula):
    
    _symbol = "<=>"
    
    def _simplify(self):
        return (self._children[0] * self._children[1]) + (-self._children[0] * -self._children[1])