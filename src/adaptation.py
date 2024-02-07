from __future__ import annotations

from .formula import Formula, Or, And, UnaryFormula, NullaryFormula, LinearConstraint, Not, ConstraintOperator
from .formulaInterpreter import FormulaInterpreter
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .revision import Revision

from fractions import Fraction

class Adaptation:

    __revision : Revision
    __domainKnowledge : set[Formula]

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, projector: Projector = None) -> None:        
        
        self.__revision = Revision(solverInit, distance, simplifiers, onlyOneSolution, projector)
        self.__domainKnowledge = set()

    def addToDK(self, knowledge : Formula):

        self.__domainKnowledge.add(knowledge)

    def removeFromDK(self, knowledge : Formula):

        self.__domainKnowledge.pop(knowledge)

    def execute(self, psi : Formula, mu : Formula):

        
        return self.__revision.execute(And(formulaSet={psi}.union(self.__domainKnowledge)), And(formulaSet={mu}.union(self.__domainKnowledge)))