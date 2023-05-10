import distanceFunction
import variableTupleDomaine
class distanceFunctionOnNumericalTuple(distanceFunction.DistanceFunction):
    def __init__(self, domaine : variableTupleDomaine.VariableTupleDomaine):
        self._domaine = domaine