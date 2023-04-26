from .Constraint import Constraint
from ....variable import Variable
from fractions import Fraction
from enum import Enum
import re

class ConstraintOperator(Enum):
    LEQ = "<="
    GEQ = ">="
    EQ = "=="

class LinearConstraint(Constraint):
    
    _symbol = None
    
    __variables: dict[Variable: Fraction]
    __operator: ConstraintOperator()
    __bound: Fraction
    
    
    """
    rules:
        - spaces doesn't matter
        - >=, == and <= only accepted operators
        - var needs to be defined before
        - var names must start with a letter and be followed by numbers or letters
        - case doesn't matter
        - always a * between var and coef
        - no need for parenthesis, brackets or whatnot
        - only accepted characters are 1234567890*/+-=<> and letters
        
    exemples:
        - 2/3*x + 3*y - z >= 12/4
        - 1 / 2 * z = = - 5
        - -3/4*y-2/3*z<=0
        
    """
    def __init__(self, string):
        
        unknownChar = re.match("[^\d a-zA-Z/\*+-<>=]")
        if unknownChar:
            raise SyntaxError(f"Unknown character {unknownChar}")
        
        # rule 1, spaces doesn't matter
        string.replace(" ", "")
        
        leftRightParts = []
        
        #rule 2, only accepted operators
        if string.find("<="):
            leftRightParts = string.split("<=")
            self.__operator = _ConstraintOperator.LEQ
        elif string.find(">="):
            leftRightParts = string.split(">=")
            self.__operator = _ConstraintOperator.GEQ
        elif string.find("=="):
            leftRightParts = string.split("==")
            self.__operator = _ConstraintOperator.EQ
        else:
            raise SyntaxError("Operator not recognized")
            
        self.__bound = Fraction(leftRightParts[1])
        
        leftRightParts[0].replace("-", "-+")
    
    def getVariables(self):
        return self._children.getKeys()
    
    def getDictVar(self):
        return self.__variables
    
    def getOperator(self):
        return self.__operator
    
    def getBound(self):
        return self.__bound