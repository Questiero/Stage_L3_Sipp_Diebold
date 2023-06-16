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
from .MLOSolver import MLOSolver

class Caron(Simplification):
    _interpreter = None
    def __init__(self, solver : MLOSolver):
        self._solver = solver

    def run(self, phi):
        if not self._interpreter.sat(phi): return phi
        if isinstance(phi, NullaryFormula): phi = And(phi)
        return self._deleteConstraint(phi)
    
    def _deleteConstraint(self, phi : Formula):
        finalConstraints : set
        finalConstraints = phi.children.copy()
        e = RealVariable("@")
        for litteral in phi.children:
            constraint : LinearConstraint
            constraint = litteral.children if isinstance(litteral, Not) else litteral
            

            finalConstraints.remove(litteral)
            newPhi = And(formulaSet=finalConstraints)
            phiTab = self.toTab(newPhi, e) 
            variables = list(newPhi.getVariables())
            variables.append(e)
            objectif = []
            for variable in variables:
                objectif.append(0 if not variable in constraint.variables.keys() else constraint.variables[variable]*-1)
            res = self._solver.solve(variables, objectif, phiTab)
            xStar = res[1]
            if res[0] == OptimizationValues.OPTIMAL:
                mustBeDeleted = False
                if isinstance(constraint, NullaryFormula):
                    sum = 0
                    for i in range(0,len(variables)): 
                        if variables[i] in constraint.variables: sum += xStar[i]*constraint.variables[variables[i]]
                    mustBeDeleted = mustBeDeleted or (sum <= constraint.bound)
                else:
                    sum = 0
                    for i in range(0,len(variables)): 
                        if variables[i] in constraint.variables: sum += xStar[i]*constraint.variables[variables[i]]*-1
                    mustBeDeleted = mustBeDeleted or (sum <= constraint.bound)
                if not mustBeDeleted: finalConstraints.add(litteral)
            else : finalConstraints.add(litteral)

        return And(formulaSet=finalConstraints)
