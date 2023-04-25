from .BinaryFormula import BinaryFormula
from ..unary.Not import Not
from ..nary.Or import Or
from ..nary.And import And

class Biconditional(BinaryFormula):
    
    _symbol = "<=>"
    
    def _simplify(self):
        return Or({And({self._children[0], self._children[1]}), And({Not(self._children[0]), Not(self._children[1])})})