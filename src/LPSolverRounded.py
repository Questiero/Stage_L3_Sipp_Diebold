from .LPSolver import LPSolver
from .constraintOperator import ConstraintOperator
from fractions import Fraction

class LPSolverRounded(LPSolver):

    __round: int

    def __init__(self, round: int = 12):
        self.__round = round
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]) -> tuple:
        
        LPsolverRes = super().solve(variables, objectif, constraints)
        res = []

        res.append(LPsolverRes[0])
        res.append([round(Fraction(x), self.__round) for x in LPsolverRes[1]])
        res.append(round(Fraction(LPsolverRes[2]), self.__round))

        return res