from .andOperator import And
from .simplification import Simplification
from .daalmans import Daalmans
from .LPSolver import LPSolver

class Projector:

    __simplifier: Simplification

    """
    By default, used simplifier is a single Daalmans using lp_solve
    """
    def __init__(self, simplification: Simplification = Daalmans(LPSolver())):
        self.__simplifier = simplification

    def projectOn(self, phi: And, variables):
        
        # First step: simplify
        phi = self.__simplifier.run(phi)

        # Second step: Find vertex

        #pb avec négations ?
        