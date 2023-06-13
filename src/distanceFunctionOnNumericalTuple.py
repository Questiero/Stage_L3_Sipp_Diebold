from distanceFunction import DistanceFunction
from variableTupleDomaine import VariableTupleDomaine
from fractions import Fraction
class distanceFunctionOnNumericalTuple(DistanceFunction):
    def __init__(self, domaine : VariableTupleDomaine):
        self._domaine = domaine

    def getW(self, i : int) -> Fraction:
        raise NotImplemented("getW is not implemented")

    def getEpsilon(self) -> Fraction:
        raise NotImplemented("getEpsilon is not implemented")