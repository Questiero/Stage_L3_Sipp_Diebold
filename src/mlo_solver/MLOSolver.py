from __future__ import annotations

from abc import ABC

class MLOSolver(ABC):
    '''
    Abstract MLOSolver class, representing mixed linear constraint solver.
    '''

    def __init__(self):
        raise NotImplementedError("Solver can't have an instance")
    def solve(self, variables : list, objectif : dict, constraints : dict) -> tuple:
        '''
        Method returning the result of a mixed linear problem.

        Attributes
        ----------
        variables : variables used in constraints
        objectif : objective function to minimize
        constraints : list of mixed linear constraints 

        Returns
        -------
        optimizationValues : OptimizationValues can be :
            INFEASIBLE if the problem is infeasible
            OPTIMAL if the solver have found an optimal value
            UNBOUNDED if the solver can found an optimal value but the problem is feasible
        '''
        raise NotImplementedError("Method solve is not implemented")