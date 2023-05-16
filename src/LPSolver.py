import MLOSolver
import constraintOperator
import integerVariable
from fractions import Fraction

import lpsolve55 as lp_solve

class LPSolver(MLOSolver.MLOSolver):
    def __init__(self):
        pass
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], constraintOperator.ConstraintOperator, Fraction]]) -> tuple:
        lp = lp_solve.lpsolve('make_lp', 0, len(variables))
        lp_solve.lpsolve('set_verbose', lp, lp_solve.IMPORTANT)

        for i in range(0,len(variables)):
            if(isinstance(variables[i], integerVariable.IntegerVariable)): 
                lp_solve.lpsolve('set_int', lp,i+1, 1)
            lp_solve.lpsolve('set_unbounded', lp, i+1)

        lp_solve.lpsolve('set_obj', lp, objectif)
        for constraint in constraints:
            comp = lp_solve.LE
            if(constraint[1] == constraintOperator.ConstraintOperator.EQ):
                comp = lp_solve.EQ
            elif (constraint[1] == constraintOperator.ConstraintOperator.GEQ):
                comp = lp_solve.GE
            lp_solve.lpsolve('add_constraint', lp, constraint[0], comp, constraint[2])

        if lp_solve.lpsolve('solve', lp) != 0:
            return (False, [], 0)
        return (True, lp_solve.lpsolve('get_variables', lp)[0], lp_solve.lpsolve('get_objective', lp))