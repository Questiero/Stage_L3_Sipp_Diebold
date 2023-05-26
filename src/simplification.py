from abc import ABC, abstractmethod

from andOperator import And
from constraintOperator import ConstraintOperator

class Simplification(ABC):
    def __init__(self, formula : And):
        self.formula = formula

    def toTab(self, formula, e):
        constraints = []
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
        constraintP = []
        for var in variables:
            if var == e: constraintP.append(-1)
            else: constraintP.append(0)
        constraints.append((constraintP, ConstraintOperator.LEQ, 0))

        return constraints

    @abstractmethod
    def run(self) -> None:
        pass
    
