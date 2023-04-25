from ..Formula import Formula

class UnaryFormula(Formula):
        
    # formula: Formula
    def __init__(self, formula):
        self._children = formula