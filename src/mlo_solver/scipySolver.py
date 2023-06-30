from __future__ import annotations

from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from .optimizationValues import OptimizationValues
from .MLOSolver import MLOSolver

from fractions import Fraction
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

class ScipySolver(MLOSolver) :
    def __init__(self):
        pass
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]) -> tuple:
        integers = []
        boundsLower = []
        boundsUpper = []
        for variable in variables: 
            integers.append(variable.isInteger())
            lower, upper = variable.getBounds()
            if(lower == None): lower = -np.inf
            if(upper == None): upper = np.inf
            boundsLower.append(lower)
            boundsUpper.append(upper)
        tab = []
        limitInf = []
        limitUp = []
        for constraint in constraints:
            tab.append(constraint[0])
            if constraint[1] == ConstraintOperator.LEQ:
                limitInf.append(-np.inf)
                limitUp.append(constraint[2])
            elif constraint[1] == ConstraintOperator.GEQ:
                limitInf.append(constraint[2])
                limitUp.append(np.inf)
            elif constraint[1] == ConstraintOperator.EQ:
                limitInf.append(constraint[2])
                limitUp.append(constraint[2])

        lc = LinearConstraint(tab, limitInf, limitUp)
        result = milp(c=objectif, integrality=integers, constraints=lc, bounds=Bounds(boundsLower, boundsUpper))
        res : tuple
        if result.status == 0:
            res = (OptimizationValues.OPTIMAL, list(result.x), result.fun)
        elif result.status == 3:
            res = (OptimizationValues.UNBOUNDED, [], float(np.inf))
        else: res = (OptimizationValues.INFEASIBLE, [], float(np.inf))
        return res