from distanceFunctionOnNumericalTuple import distanceFunctionOnNumericalTuple
from l1DistanceFunction import l1DistanceFunction
from fractions import Fraction
from math import ceil
from domain import Domain
class discreteL1DistanceFunction(distanceFunctionOnNumericalTuple):
    def __init__(self, w:dict[Fraction], epsilon : Fraction, domaine : Domain = None):
        self._distance = l1DistanceFunction(w, domaine)
        self._epsilon = epsilon
    def dist(self, x : tuple, y : tuple):
        return self._epsilon * ceil(self._distance.dist(x,y) / self._epsilon)
    
    def getW(self, i : int) -> Fraction:
        return self._distance.getW(i)

    def getEpsilon(self) -> Fraction:
        return self._epsilon