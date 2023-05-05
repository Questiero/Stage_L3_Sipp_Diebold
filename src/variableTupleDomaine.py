import variable
import domaine
class VariableTupleDomaine(domaine.Domaine):
    def __init__(self, *variable : variable.Variable):
        self._variable = variable
