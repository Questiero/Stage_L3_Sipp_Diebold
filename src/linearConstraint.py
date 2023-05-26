from __future__ import annotations # used to type hint the class itself

from constraint import Constraint
from variableManager import VariableManager
from constraintOperator import ConstraintOperator

from fractions import Fraction

import re

# Typing only imports
from variable import Variable

class LinearConstraint(Constraint):
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
    children: None
        The children of the current node. Since a cosntraint doesn't have any,
        it's None.
    _symbol: None
        The symbol used to represent the constraint syntaxically. Since it's doesn't
        have any, it's None.
    '''
    
    variables: dict[Variable, Fraction]
    operator: ConstraintOperator
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
            self.operator = ConstraintOperator.LEQ
        elif string.find(">=") != -1:
            leftRightParts = string.split(">=")
            self.operator = ConstraintOperator.GEQ
        elif string.find("=") != -1:
            leftRightParts = string.split("=")
            self.operator = ConstraintOperator.EQ
        else:
            raise SyntaxError("Operator not recognized")

        if leftRightParts[1] == "":
            raise SyntaxError("Bound not found")
        else:
            self.bound = Fraction(leftRightParts[1])
        
        leftRightParts[0] = leftRightParts[0].replace("-", "+-")
        leftRightParts[0] = leftRightParts[0].replace("++", "+")
        if leftRightParts[0].find("+-") == 0:
            leftRightParts[0] = leftRightParts[0][1:]
        splitLeft = leftRightParts[0].split("+")
        
        for split in splitLeft:
            
            var = None
            coef = None
            
            if split.find("*") != -1:
                (coefString, varName) = split.split("*")
                if(varName != "@"):
                    var = VariableManager.get(varName)
                    coef = Fraction(coefString)
            else:
                if split[0] == "-":
                    coef = Fraction("-1")
                    var = VariableManager.get(split[1:])
                else:
                    coef = Fraction("1")
                    var = VariableManager.get(split)
            
            if var in self.variables:
                raise ValueError(f"Duplicate variable {var._name} found")
            elif var != None:
                self.variables[var] = coef

    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self.variables.keys()
    
    def getAdherence(self, var : Variable) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        return [[self]]

    def _getAdherenceNeg(self, var : Variable)  -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        copyConstrainte = self.clone()

        copyConstrainte.variables[var] = Fraction(1,1)
        res = [[copyConstrainte]]

        return res
    
    def getTuple(self, variables : list) -> tuple:
        """
        
        """
        tabVar = []
        op = self.operator
        bound = self.bound
        for variable in variables:
            if not variable in self.variables: tabVar.append(0)
            else: tabVar.append(self.variables[variable])

        if(op == ConstraintOperator.GEQ):
            for i in range(0, len(tabVar)-1):
                tabVar[i] *= -1
            bound *= -1
            op = ConstraintOperator.LEQ
        
        return (tabVar, op, bound)
    
    def __str__(self):
        s = ""
        for var, coef in self.variables.items():
            s += str(coef) + "*" + str(var) + " + "
        s = s[:-2]
        s += str(self.operator.value) + " "
        s += str(self.bound)
        return s
            
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        from andOperator import And
        res = LinearConstraint(str(self))

        if self.operator == ConstraintOperator.GEQ :
            for variable in res.variables.keys():
                res.variables[variable] *= -1
            res.bound *= -1
            res.operator = ConstraintOperator.LEQ
        elif self.operator == ConstraintOperator.EQ:
            res = [LinearConstraint(str(self))]
            res[0].operator = ConstraintOperator.GEQ
            res.append(res[0].toLessOrEqConstraint())
            res[0].operator = ConstraintOperator.LEQ
            res = And(formulaSet=set(res))

        return res
    
    def clone(self) -> LinearConstraint:
        return LinearConstraint(str(self))
    
    def replace(self, variable : Variable, num : Fraction):
        if variable in self.variables:
            self.bound = self.bound - num * self.variables[variable]
            del self.variables[variable]
        if len(self.variables) == 0: raise IndexError("Not enough values in constraint")

    def __eq__(self, o) -> bool:
        
        if o.__class__ != self.__class__:
            return False
        elif (o.variables != self.variables) | (o.operator != self.operator) | (o.bound != self.bound):
            return False
        else:
            return True
        
    def __hash__(self):
        return hash(str(self))