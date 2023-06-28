from .simplificator import Simplificator
from ..formula import Formula
from ..variable.realVariable import RealVariable
from ..formula.nullaryFormula.constraint.linearConstraint import LinearConstraint
from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from ..formula.unaryFormula.notOperator import Not
from..formula.naryFormula.andOperator import And
from ..mlo_solver.optimizationValues import OptimizationValues
from..formula.nullaryFormula.nullaryFormula import NullaryFormula
from fractions import Fraction
from ..mlo_solver.MLOSolver import MLOSolver

class Caron(Simplificator):
    _interpreter = None
    def __init__(self, solver : MLOSolver):
        self._solver = solver

    def run(self, phi):
        if not self._interpreter.sat(phi): return phi
        if isinstance(phi, NullaryFormula): phi = And(phi)
        return self._deleteConstraint(phi)
    
    def _deleteConstraint(self, phi : Formula):
        finalConstraints : list
        finalConstraints = list(phi.children.copy())
        e = RealVariable("@")
        variables = list(phi.getVariables())
        variables.append(e)
        for litteral in phi.children:
            constraint : LinearConstraint
            constraint = litteral.children if isinstance(litteral, Not) else litteral
            

            finalConstraints.remove(litteral)
            newPhi = And(*finalConstraints)
            phiTab = self.toTab(newPhi, e, variables=variables) 
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
                    mustBeDeleted = (sum <= constraint.bound)
                else:
                    sum = 0
                    for i in range(0,len(variables)): 
                        if variables[i] in constraint.variables: sum += xStar[i]*constraint.variables[variables[i]]*-1
                    mustBeDeleted = (sum < constraint.bound)
                if not mustBeDeleted: finalConstraints.append(litteral)
            else : finalConstraints.append(litteral)

        return And(*finalConstraints)
