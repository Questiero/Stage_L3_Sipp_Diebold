"""
Abstract class, representing a simplificator of conjunction of litterals.
"""

from __future__ import annotations

from ..formula import And, ConstraintOperator

from abc import ABC, abstractmethod

class Simplificator(ABC):
    def __init__(self, formula : And):
        self.formula = formula

    def toTab(self, formula, e, variables : list = None ):
        constraints = []
        if variables == None : 
            variables = list(formula.getVariables())
            variables.append(e)
        for lc in formula.getAdherence(e):
            for constraint in lc:
                constraintP = []
                for variable in variables:
                    if variable in constraint.variables:
                        constraintP.append(constraint.variables[variable])
                    else:
                        constraintP.append(0)
                constraints.append((constraintP, constraint.operator, constraint.bound))
        lastConstraint = []
        for variable in variables: 
            lastConstraint.append(-1 if variable == e else 0)
        return constraints + [(lastConstraint, ConstraintOperator.LEQ, 0)]

    @abstractmethod
    def run(self) -> None:
        pass
    
