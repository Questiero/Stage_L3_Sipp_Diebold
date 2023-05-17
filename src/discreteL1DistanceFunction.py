from distanceFunctionOnNumericalTuple import DistanceFunctionOnNumericalTuple
from l1DistanceFunction import L1DistanceFunction
from fractions import Fraction
from math import ceil
class discreteL1DistanceFunction(DistanceFunctionOnNumericalTuple):
    def __init__(self, *w, epsilon : Fraction):
        self._distance = L1DistanceFunction(*w)
        self._epsilon = epsilon
    def dist(self, x : tuple, y : tuple):
        return self._epsilon * ceil(self._distance.dist(x,y) / self._epsilon)