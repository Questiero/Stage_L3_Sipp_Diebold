from .simplification import Simplification
from .formula import Formula
from .realVariable import RealVariable
from .linearConstraint import LinearConstraint
from .constraintOperator import ConstraintOperator
from .notOperator import Not
from.andOperator import And
from .optimizationValues import OptimizationValues
from.nullaryFormula import NullaryFormula
from fractions import Fraction

class Daalmans(Simplification):
    _interpreter = None
    def __init__(self, solver):
        self._solver = solver
    
    def run(self, phi):
        if not self._interpreter.sat(phi): return phi
        if isinstance(phi, NullaryFormula): phi = And(phi)
        phiPrime = self.fixedVariables(phi)
        phiPrime = self.deleteConstraint(phiPrime)
        return phiPrime
    
    def fixedVariables(self, phi : Formula) -> Formula:
        variablesToAnalyse = list(phi.getVariables())
        objectivFunction = [0] * (len(variablesToAnalyse) + 1)
        index = 0
        e = RealVariable("@")
        tabPhi = self.toTab(phi, e)
        variables = variablesToAnalyse + [e]
        fixedVariables = {}

        # For each variable x 
        for variable in variablesToAnalyse:
            # We will analyse the optimal value of the variable when we wants to maximize x and minimize x
            objectivFunction[index] = 1
            v1 = self.solve(variables, objectivFunction, tabPhi)
            objectivFunction[index] = -1
            v2 = self.solve(variables, objectivFunction, tabPhi)
            objectivFunction[index] = 0
            if v1[0] == OptimizationValues.OPTIMAL and v2[0] == OptimizationValues.OPTIMAL and v1[1][index] == v2[1][index] :
                # If x can have only one value, it is a fixed variable
                fixedVariables[variable] = Fraction(v1[1][index])

            index += 1
        return self.__removeVariables(phi, fixedVariables)

    def __removeVariables(self, phi : Formula, fixedVariables : dict):
        for variable in fixedVariables.keys():
            newChildren = set()
            for litteral in phi.children:
                try:
                    if isinstance(litteral, Not) :
                        litteral.children.replace(variable, -fixedVariables[variable])
                    else:
                        litteral.replace(variable, fixedVariables[variable])
                    newChildren.add(litteral)
                except:
                    # If the constraint is now useless, we dont keep it in the children of the formula
                    pass
            phi.children = newChildren
            
            # We adding = constraint between x and his only possible value
            newConstraint =  LinearConstraint("")
            newConstraint.variables[variable] = 1
            newConstraint.operator = ConstraintOperator.EQ
            newConstraint.bound = fixedVariables[variable]
            phi = phi & newConstraint
        return phi
            

    def deleteConstraint(self, phi : Formula) -> Formula:
        actualConstraints : set
        actualConstraints = phi.children.copy()
        for constraint in phi.children:
            actualConstraints.remove(constraint)

            actualConstraints.add(~constraint)
            form = And(formulaSet=actualConstraints).toLessOrEqConstraint().toDNF()
            if self._interpreter.sat(form) :
                actualConstraints.add(constraint)
            actualConstraints.remove(~constraint)

        return And(formulaSet=actualConstraints)

    
    def solve(self, variables, obj, constraints):
        return self._solver.solve(variables, obj, constraints)

