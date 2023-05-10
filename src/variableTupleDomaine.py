import variable
import domain
class VariableTupleDomaine(domain.Domain):
    def __init__(self, *variable : variable.Variable):
        self._variable = variable
