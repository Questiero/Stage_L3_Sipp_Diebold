from distanceFunction import DistanceFunction
from variableTupleDomaine import VariableTupleDomaine
class distanceFunctionOnNumericalTuple(DistanceFunction):
    def __init__(self, domaine : VariableTupleDomaine):
        self._domaine = domaine