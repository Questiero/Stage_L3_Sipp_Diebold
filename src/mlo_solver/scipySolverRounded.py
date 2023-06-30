from __future__ import annotations

from .scipySolver import ScipySolver
from ..formula.nullaryFormula.constraint import ConstraintOperator

from fractions import Fraction
import numpy as np

class ScipySolverRounded(ScipySolver):

    __round: int

    def __init__(self, round: int = 12):
        self.__round = round
        
    def solve(self, variables : list, objectif : dict, constraints : dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]) -> tuple:
        
        scipySolverRes = super().solve(variables, objectif, constraints)
        res = []

        res.append(scipySolverRes[0])
        res.append([round(Fraction(x), self.__round) for x in scipySolverRes[1]])

        if np.isinf(scipySolverRes[2]):
            res.append(scipySolverRes[2])
        else:
            res.append(round(Fraction(scipySolverRes[2]), self.__round))

        return res