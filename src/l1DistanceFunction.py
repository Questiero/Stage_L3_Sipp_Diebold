import distanceFunctionOnNumericalTuple
from fractions import Fraction
class l1DistanceFunction(distanceFunctionOnNumericalTuple.distanceFunctionOnNumericalTuple):
    def __init__(self, *w : Fraction):
        self._fractions = w
    def dist(self, x : tuple, y :tuple):
        if(len(x) != len(y)): raise Exception("x and y are not in the same domaine")
        res = 0
        for i in range(0, len(x)):
            res += self._fractions[i] * abs(x[i] - y[i])
        return res