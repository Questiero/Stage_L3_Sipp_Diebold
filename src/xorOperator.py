import binaryFormula
import notOperator
import orOperator
import ndOperator

class Xor(binaryFormula.BinaryFormula):
    
    _symbol = "XOR"
    
    def _simplify(self):
        return orOperator.Or({ndOperator.And({self._children[0], notOperator.Not(self._children[1])}), ndOperator.And({notOperator.Not(self._children[0]), self._children[1]})})