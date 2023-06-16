from .variable import Variable
from .domain import Domain

class VariableTupleDomaine(Domain):
    def __init__(self, *variable : Variable):
        self._variable = variable
