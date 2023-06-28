from .andOperator import And
from .variable import Variable

from abc import ABC, abstractmethod

class Projector (ABC):

    @abstractmethod
    def projectOn(self, phi: And, variables: set[Variable]):
        pass