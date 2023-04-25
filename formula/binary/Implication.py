from .BinaryFormula import BinaryFormula
from ..unary.Not import Not
from ..nary.Or import Or

class Implication(BinaryFormula):
    
    _symbol = "=>"
    
    def _simplify(self):
        return Or({Not(self._children[0], self._children[1])})