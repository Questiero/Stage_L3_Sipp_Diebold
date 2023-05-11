import MLOSolver
import constraintOperator
import integerVariable

import lpsolve55 as lp_solve

class LPSolver(MLOSolver.MLOSolver):
    def __init__(self):
        pass
        
    def solve(self, variables : list, objectif : dict, constraints : dict) -> tuple:
        lp = lp_solve.lpsolve('make_lp', 0, len(variables))
        lp_solve.lpsolve('set_verbose', lp, lp_solve.IMPORTANT)

        for variable in variables:
            if(isinstance(variable, integerVariable.IntegerVariable)): 
                lp_solve.lpsolve('set_int', lp,variables.index(variable)+1, 1)

        lp_solve.lpsolve('set_obj', lp, objectif)
        for constraint in constraints:
            constraintP = []
            for variable in variables:
                if variable in constraint.variables:
                    constraintP.append(constraint.variables[variable])
                else:
                    constraintP.append(0)
            comp = lp_solve.LE
            if(constraint.operator == constraintOperator.ConstraintOperator.EQ):
                comp = lp_solve.EQ
            elif (constraint.operator == constraintOperator.ConstraintOperator.GEQ):
                comp = lp_solve.GE
            lp_solve.lpsolve('add_constraint', lp, constraintP, comp, constraint.bound)

        if lp_solve.lpsolve('solve', lp) != 0:
            return (False, [], 0)
        return (True, lp_solve.lpsolve('get_variables', lp)[0], lp_solve.lpsolve('get_objective', lp))