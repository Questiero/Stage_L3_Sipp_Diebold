"""
Created on Thu Apr 20 11:03:01 2023

@author: di3bold
"""
from solver.Solver import *
from formula.nullary.constraint.LinearConstraint import *
import lpsolve55 as lp_solve
class LPSolver(Solver):
    _variables = []
    def __init__(self, variables : list):
        self._variables =  variables
        
    def solve(self,constraints : dict) -> tuple:
        lp = lp_solve.lpsolve('make_lp', 0, 2)
        lp_solve.lpsolve('set_verbose', lp, lp_solve.IMPORTANT)
        objectif = []
        for variable in self._variables:
            objectif.append(-1)

        lp_solve.lpsolve('set_obj', lp, objectif)

        for constraint in constraints:
            constraintP = []
            for variable in self._variables:

                constraintP.append(constraint.getDictVar()[variable])
            comp = lp_solve.LE
            if(constraint.getOperator() == ConstraintOperator.EQ):
                comp = lp_solve.EQ
            elif (constraint.getOperator() == ConstraintOperator.GEQ):
                comp = lp_solve.GE
            lp_solve.lpsolve('add_constraint', lp, constraintP, comp, constraint.getBound())

        if lp_solve.lpsolve('solve', lp) != 0:
            raise Exception("No optimisable")
        return lp_solve.lpsolve('get_variables', lp)[0]