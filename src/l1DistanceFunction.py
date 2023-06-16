from .distanceFunctionOnNumericalTuple import distanceFunctionOnNumericalTuple
from .domain import Domain
from .variable import Variable

from fractions import Fraction

class l1DistanceFunction(distanceFunctionOnNumericalTuple):

    _weights : dict[Variable, Fraction]

    def __init__(self, weights : dict[Variable, Fraction], domaine : Domain = None):
        self._domaine = domaine
        self._weights = weights

    def dist(self, x : tuple, y :tuple):
        if(len(x) != len(y)): raise Exception("x and y are not in the same domaine")
        res = 0
        for i in range(0, len(x)):
            res += self._fractions[i] * abs(x[i] - y[i])
        return res

    def getWeights(self) -> Fraction:
        return self._weights

    def getEpsilon(self) -> Fraction:
        return Fraction(1,1)