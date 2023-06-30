from __future__ import annotations

from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from .optimizationValues import OptimizationValues
from .MLOSolver import MLOSolver

from fractions import Fraction
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint, NonlinearConstraint

class ScipySolver(MLOSolver) :
    def __init__(self):
        pass
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]) -> tuple:
        integers = []
        for variable in variables: 
            integers.append(variable.isInteger())
        tab = []
        limitInf = []
        limitUp = []
        for constraint in constraints:
            tab.append(constraint[0])
            limitInf.append(-np.inf)
            limitUp.append(constraint[2])

        lc = LinearConstraint(tab, limitInf, limitUp)
        result = milp(c=objectif, integrality=integers, constraints=lc)
        res : tuple
        if result.status == 0:
            res = (OptimizationValues.OPTIMAL, list(result.x), result.fun)
        elif result.status == 3:
            res = (OptimizationValues.UNBOUNDED, [], np.inf)
        else: res = (OptimizationValues.INFEASIBLE, [], np.inf)
        return res