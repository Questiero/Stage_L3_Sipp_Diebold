from .binaryFormula import BinaryFormula
from ..unary.notOperator import Not
from ..nary.orOperator import Or
from ..nary.andOperator import And

class Xor(BinaryFormula):
    
    _symbol = "XOR"
    
    def _simplify(self):
        return Or({And({self._children[0], Not(self._children[1])}), And({Not(self._children[0]), self._children[1]})})