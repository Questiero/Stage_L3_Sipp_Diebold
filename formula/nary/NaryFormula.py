from ..Formula import Formula

class NaryFormula(Formula):
    
    # formula: Set(Formula)
    def __init__(self, formulaSet):
        self._children = formulaSet