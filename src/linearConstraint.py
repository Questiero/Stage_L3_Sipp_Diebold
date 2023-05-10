import constraint
import variableManager
import constraintOperator

from fractions import Fraction

import re

# Typing only imports
import variable

class LinearConstraint(constraint.Constraint):
    '''
    Abstract Constraint class, representing a Constraint in PCMLC.

    Parameters
    ----------
    string: String
        The linear constraint you want to define, following the syntax rules:
            - only accepted characters are 1234567890*/+-=<>. and letters
            - spaces doesn't matter
            - >=, = and <= only accepted operators
            - var needs to be defined before
            - var names must start with a letter and be followed by numbers or letters
            - case matters
            - always a * between var and coef
            - no duplicates variables in the same constraint
            
    Raises
    ------
    SyntaxError
        If the syntax of string is wrong.
        
    Attributes
    ----------
    variables: dict[Variable, Fraction]
        The variables in the constraint, associated with their coefficient
    operator: ConstraintOperator
        The operator of the constraint
    bound: Fraction
        The bound of the constraint
    _children: None
        The children of the current node. Since a cosntraint doesn't have any,
        it's None.
    _symbol: None
        The symbol used to represent the constraint syntaxically. Since it's doesn't
        have any, it's None.
    '''
    
    variables: dict[variable.Variable, Fraction]
    operator: constraintOperator.ConstraintOperator
    bound: Fraction
    
    def __init__(self, string: str):
        self.variables = {}
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
            self.operator = constraintOperator.ConstraintOperator.LEQ
        elif string.find(">=") != -1:
            leftRightParts = string.split(">=")
            self.operator = constraintOperator.ConstraintOperator.GEQ
        elif string.find("=") != -1:
            leftRightParts = string.split("=")
            self.operator = constraintOperator.ConstraintOperator.EQ
        else:
            raise SyntaxError("Operator not recognized")

        if leftRightParts[1] == "":
            raise SyntaxError("Bound not found")
        else:
            self.bound = Fraction(leftRightParts[1])
        
        leftRightParts[0] = leftRightParts[0].replace("-", "+-")
        if leftRightParts[0].find("+-") == 0:
            leftRightParts[0] = leftRightParts[0][1:]
        splitLeft = leftRightParts[0].split("+")
        
        for split in splitLeft:
            
            var = None
            coef = None
            
            if split.find("*") != -1:
                (coefString, varName) = split.split("*")
                var = variableManager.VariableManager.get(varName)
                coef = Fraction(coefString)
            else:
                if split[0] == "-":
                    coef = Fraction("-1")
                    var = variableManager.VariableManager.get(split[1:])
                else:
                    coef = Fraction("1")
                    var = variableManager.VariableManager.get(split)
            
            if var in self.variables:
                raise ValueError(f"Duplicate variable {var._name} found")
            else:
                self.variables[var] = coef
    
    def getVariables(self) -> set[variable.Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self.variables.keys()
    
    def getAdherence(self) -> list[list[constraint.Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        
        return [[self]]
    
    def _getAdherenceNeg(self) -> list[list[constraint.Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        
        if(self.operator == constraintOperator.ConstraintOperator.EQ): return []
        elif(self.operator == constraintOperator.ConstraintOperator.LEQ):
            self.operator = constraintOperator.ConstraintOperator.GEQ
        elif(self.operator == constraintOperator.ConstraintOperator.GEQ):
            self.operator = constraintOperator.ConstraintOperator.LEQ

        return [[self]]
    
    def __str__(self):
        s = "("
        for var, coef in self.variables.items():
            s += str(coef) + "*" + str(var) + " + "
        s = s[:-2]
        s += str(self.operator.value) + " "
        s += str(self.bound) + ")"
        return s
            
