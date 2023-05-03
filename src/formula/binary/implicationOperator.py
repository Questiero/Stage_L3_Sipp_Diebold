from .binaryFormula import BinaryFormula
from ..unary.notOperator import Not
from ..nary.orOperator import Or

class Implication(BinaryFormula):
    
    _symbol = "=>"
    
    def _simplify(self):
        return Or({Not(self._children[0], self._children[1])})