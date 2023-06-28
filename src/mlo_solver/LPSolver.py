from __future__ import annotations

from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from .optimizationValues import OptimizationValues
from .MLOSolver import MLOSolver

from fractions import Fraction
import lpsolve55 as lp_solve

class LPSolver(MLOSolver):
    def __init__(self):
        pass
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]) -> tuple:
        lp = lp_solve.lpsolve('make_lp', 0, len(variables))
        lp_solve.lpsolve('set_verbose', lp, lp_solve.IMPORTANT)

        for i in range(0,len(variables)):
            if(variables[i].isInteger()): 
                lp_solve.lpsolve('set_int', lp,i+1, 1)

            haveBoundL, haveBoundR = variables[i].haveBound()
            if(not haveBoundL and not haveBoundR):
                lp_solve.lpsolve('set_unbounded', lp, i+1)
            else:
                lower, upper = variables[i].getBounds()
                if(lower == None): lower = -1e30
                if(upper == None): upper = 1e30
                lp_solve.lpsolve('set_bounds', lp, i+1)

        lp_solve.lpsolve('set_obj', lp, objectif)
        for constraint in constraints:
            comp = lp_solve.LE
            if(constraint[1] == ConstraintOperator.EQ):
                comp = lp_solve.EQ
            elif (constraint[1] == ConstraintOperator.GEQ):
                comp = lp_solve.GE
            lp_solve.lpsolve('add_constraint', lp, constraint[0], comp, constraint[2])
        tmp = lp_solve.lpsolve('solve', lp)
        if tmp not in [0,3]:
            return (OptimizationValues.INFEASIBLE, [], 0)
        if tmp == 3:
            val = lp_solve.lpsolve('get_variables', lp)[0]
            return (OptimizationValues.UNBOUNDED, val, lp_solve.lpsolve('get_objective', lp))
        return (OptimizationValues.OPTIMAL, lp_solve.lpsolve('get_variables', lp)[0], lp_solve.lpsolve('get_objective', lp))