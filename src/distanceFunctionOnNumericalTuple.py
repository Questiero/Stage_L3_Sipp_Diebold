import distanceFunction
import variableTupleDomaine
class distanceFunctionOnNumericalTuple(distanceFunction):
    def __init__(self, domaine : variableTupleDomaine.VariableTupleDomaine):
        self._domaine = domaine