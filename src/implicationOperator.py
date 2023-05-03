import binaryFormula
import notOperator
import orOperator

class Implication(binaryFormula.BinaryFormula):
    
    _symbol = "=>"
    
    def _simplify(self):
        return orOperator.Or({notOperator.Not(self._children[0], self._children[1])})