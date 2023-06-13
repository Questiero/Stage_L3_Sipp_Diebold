from distanceFunctionOnNumericalTuple import distanceFunctionOnNumericalTuple
from domain import Domain

from fractions import Fraction

class l1DistanceFunction(distanceFunctionOnNumericalTuple):
    def __init__(self, w : dict[Fraction], domaine : Domain = None):
        self._domaine = domaine
        self._fractions = w
    def dist(self, x : tuple, y :tuple):
        if(len(x) != len(y)): raise Exception("x and y are not in the same domaine")
        res = 0
        for i in range(0, len(x)):
            res += self._fractions[i] * abs(x[i] - y[i])
        return res

    def getW(self, i : int) -> Fraction:
        return self._fractions[i]

    def getEpsilon(self) -> Fraction:
        return Fraction(1,1)