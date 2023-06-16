from .andOperator import And
from .simplification import Simplification
from .daalmans import Daalmans
from .LPSolver import LPSolver
from .constraintOperator import ConstraintOperator
from .notOperator import Not

from .variable import Variable

import itertools
import numpy as np
from fractions import Fraction

class Projector:

    __simplifier: Simplification

    """
    By default, used simplifier is a single Daalmans using lp_solve
    """
    def __init__(self, simplification: Simplification = Daalmans(LPSolver())):
        self.__simplifier = simplification

    def projectOn(self, phi: And, variables: set[Variable]):

        #TODO Négation ?

        # First step: simplify
        # phi = self.__simplifier.run(phi)

        # Second step: Get all variables
        variables = list(phi.getVariables())

        # Second step: Get all hyperplanes
        hyperplanes = list()

        for miniPhi in phi.children:

            hypVar = np.array([])

            if (isinstance(miniPhi, Not)):
                c = miniPhi.children.clone()
            else:
                c = miniPhi.clone()
            
            for var in variables:
                v = c.variables.get(var)
                if (v):
                    hypVar = np.append(hypVar, v)
                else:
                    hypVar = np.append(hypVar, Fraction("0"))

            hyperplanes.append((hypVar, c.bound))

        # Third step: Get all non parallel combinations
        nonParallelCombinations = list()

        for hyperplaneCombination in itertools.combinations(hyperplanes, len(phi.getVariables())):
                
            foundParallel = False

            for combinationPair in itertools.combinations(hyperplaneCombination, 2):

                one = combinationPair[0][0]
                two = combinationPair[1][0]

                if np.dot(one,two)*np.dot(one,two) == np.dot(one,one)*np.dot(two,two):
                    foundParallel = True
                    break

            if not foundParallel:
                nonParallelCombinations.append(hyperplaneCombination)

        # Fourth step: Get all vertex from combinations


        # Fifth step: Get outside vertex
        