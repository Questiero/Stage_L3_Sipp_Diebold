import binaryFormula
import notOperator
import orOperator
import andOperator

class Xor(binaryFormula.BinaryFormula):
    
    _symbol = "XOR"
    
    def _simplify(self):
        return orOperator.Or({andOperator.And({self._children[0], notOperator.Not(self._children[1])}), andOperator.And({notOperator.Not(self._children[0]), self._children[1]})})