from .distanceFunctionOnNumericalTuple import distanceFunctionOnNumericalTuple
from .l1DistanceFunction import l1DistanceFunction
from ..domain import Domain
from ...variable import Variable

from fractions import Fraction
from math import ceil

class discreteL1DistanceFunction(distanceFunctionOnNumericalTuple):

    def __init__(self, weights : dict[Variable, Fraction], epsilon : Fraction = Fraction("1e-6"), domaine : Domain = None):
        self._distance = l1DistanceFunction(weights, domaine)
        self._epsilon = epsilon

    def dist(self, x : tuple, y : tuple):
        return self._epsilon * ceil(self._distance.dist(x,y) / self._epsilon)
    
    def getWeights(self) -> Fraction:
        return self._distance.getWeights()
    
    def getEpsilon(self) -> Fraction:
        return self._epsilon