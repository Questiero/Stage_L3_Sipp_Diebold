import binaryFormula
import notOperator
import orOperator
import andOperator

class Xor(binaryFormula.BinaryFormula):
    
    _symbol = "XOR"
    
    def _simplify(self):
        return (self._children[0] * -self._children[1]) + (-self._children[0] * self._children[1])