from distanceFunction import DistanceFunction
from variableTupleDomaine import VariableTupleDomaine
from fractions import Fraction

from abc import abstractmethod

class distanceFunctionOnNumericalTuple(DistanceFunction):

    def __init__(self, domaine : VariableTupleDomaine):
        self._domaine = domaine

    @abstractmethod
    def getWeights(self) -> Fraction:
        pass

    @abstractmethod
    def getEpsilon(self) -> Fraction:
        pass