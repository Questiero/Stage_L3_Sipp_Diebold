import constraint
import variable
import variableManager

from fractions import Fraction
from enum import Enum

import re

class ConstraintOperator(Enum):
    LEQ = "<="
    GEQ = ">="
    EQ = "="

class LinearConstraint(constraint.Constraint):
    
    _symbol = None

    __variables: dict
    __operator: ConstraintOperator
    __bound: Fraction
    
    
    """
    rules:
        - only accepted characters are 1234567890*/+-=<>. and letters
        - spaces doesn't matter
        - >=, = and <= only accepted operators
        - var needs to be defined before
        - var names must start with a letter and be followed by numbers or letters
        - case doesn't matter
        - always a * between var and coef
        - no duplicates variables in the same constraint
        
    exemples:
        - 2/3*x + 3*y - z >= 12/4
        - 1 / 2 * x + z = = - 5.3
        - -3/4*y-2/3*z<=0
        
    """
    def __init__(self, string):
        self.__variables = {}
        # rule 1, only accepted characters 
        unknownChar = re.match(r"[^\d a-zA-Z/\*+\-<>=\.]", string)
        if unknownChar:
            raise SyntaxError(f"Unknown character {unknownChar}")
        
        # rule 2, spaces doesn't matter
        string = re.sub('\s*','', string)
        
        leftRightParts = []
        
        #rule 3, only accepted operators
        if string.find("<=") != -1:
            leftRightParts = string.split("<=")
            self.__operator = ConstraintOperator.LEQ
        elif string.find(">=") != -1:
            leftRightParts = string.split(">=")
            self.__operator = ConstraintOperator.GEQ
        elif string.find("=") != -1:
            leftRightParts = string.split("=")
            self.__operator = ConstraintOperator.EQ
        else:
            raise SyntaxError("Operator not recognized")

        if leftRightParts[1] == "":
            raise SyntaxError("Bound not found")
        else:
            self.__bound = Fraction(leftRightParts[1])
        
        leftRightParts[0].replace("-", "+-")
        splitLeft = leftRightParts[0].split("+")
        
        for split in splitLeft:
            
            var = None
            coef = None
            
            if split.find("*"):
                (coefString, varName) = split.split("*")
                var = variableManager.VariableManager.get(varName.lower())
                coef = Fraction(coefString)
            else:
                if split[0] == "-":
                    coef = Fraction("-1")
                    var = variableManager.VariableManager.get(split[1:].lower())
                else:
                    coef = Fraction("1")
                    var = variableManager.VariableManager.get(split.lower())
            
            if var in self.__variables:
                raise ValueError(f"Duplicate variable {var._name} found")
            else:
                self.__variables[var] = coef
                
    def __str__(self):
        s = ""
        for var, coef in self.__variables.items():
            s += str(coef) + "*" + str(var) + " + "
        s = s[:-2]
        s += str(self.__operator.value) + " "
        s += str(self.__bound)
        return s
    
    def getVariables(self):
        return self.__variables.keys()
    
    def getDictVar(self):
        return self.__variables
    
    def getOperator(self):
        return self.__operator
    
    def getBound(self):
        return self.__bound
    
    def getConstraintGonfle(self):
        return [[self]]
    
    def getConstraintGonfleNeg(self):
        if(self.__operator == ConstraintOperator.EQ): return []
        elif(self.__operator == ConstraintOperator.LEQ):
            self.__operator = ConstraintOperator.GEQ
        elif(self.__operator == ConstraintOperator.GEQ):
            self.__operator = ConstraintOperator.LEQ

        return [[self]]
            