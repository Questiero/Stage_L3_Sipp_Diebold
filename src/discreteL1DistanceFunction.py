import distanceFunctionOnNumericalTuple
import l1DistanceFunction
from fractions import Fraction
from math import ceil
class discreteL1DistanceFunction(distanceFunctionOnNumericalTuple):
    def __init__(self, *w, epsilon : Fraction):
        self._distance = l1DistanceFunction(w)
        self._epsilon = epsilon
    def dist(self, x : tuple, y : tuple):
        return self._epsilon * ceil(self._distance.dist(x,y) / self._epsilon)