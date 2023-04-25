from .Constraint import Constraint
from ....variable import Variable
from fractions import Fraction
from enum import Enum

class _ConstraintSymbol(Enum):
    LEQ: "<="
    GEQ: ">="
    EQ: "=="

class LinearConstraint(Constraint):
    
    _symbol = None
    
    __variables: dict[Variable: Fraction]
    __sign = _ConstraintSymbol
    __limit = Fraction
    
    def __init__(self, string):
        #TODO Parser
        pass
    
    def getVariables(self):
        return self._children.getKeys()