from .andOperator import And
from .simplification import Simplification
from .daalmans import Daalmans
from .LPSolver import LPSolver
from .constraintOperator import ConstraintOperator
from .notOperator import Not

from .variable import Variable

import itertools
import numpy as np
from scipy.spatial import ConvexHull
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
        phi = self.__simplifier.run(phi)

        # Second step: Get all variables
        allVariables = list(phi.getVariables())

        # Third step: Get all hyperplanes
        hyperplanes = list()

        for miniPhi in phi.children:

            hypVar = np.array([])

            if (isinstance(miniPhi, Not)):
                c = miniPhi.children.clone()
            else:
                c = miniPhi.clone()
            
            for var in allVariables:
                v = c.variables.get(var)
                if (v):
                    hypVar = np.append(hypVar, v)
                else:
                    hypVar = np.append(hypVar, Fraction(0))

            hyperplanes.append((hypVar, c.bound))

        # Fourth step: Get all non parallel combinations
        nonParallelCombinations = list(itertools.combinations(hyperplanes, len(phi.getVariables())))

      #  for hyperplaneCombination in itertools.combinations(hyperplanes, len(phi.getVariables())):
      #          
       #     foundParallel = False
#
       #     for combinationPair in itertools.combinations(hyperplaneCombination, 2):
#
       #         x = combinationPair[0][0]
       #         y = combinationPair[1][0]
#
       #         if (np.dot(x,y)*np.dot(x,y) == np.dot(x,x)*np.dot(y,y)):
       #             foundParallel = True
        #            break
#
        #    if not foundParallel:
        #        nonParallelCombinations.append(hyperplaneCombination)

        # Fifth step: Get all vertex from combinations
        vertex = list()

        for comb in nonParallelCombinations:
            a = []
            b = []
            for hyperplane in comb:
                a.append([float(x) for x in hyperplane[0]])
                b.append(float(hyperplane[1]))

            try:
                vertex.append(np.linalg.solve(a, b))    
            except (np.linalg.LinAlgError):
                pass

        vertex = np.array(vertex)
        
        # Sixth step: project all vertex
        variablesToProject = np.array([], dtype=bool)
        for var in allVariables:
            if var in variables:
                variablesToProject = np.append(variablesToProject, True)
            else:
                variablesToProject = np.append(variablesToProject, False)

        projectedVertex = list()
        for v in vertex:
            print(v[variablesToProject])
            projectedVertex.append(v[variablesToProject])

        projectedVertex = np.array(projectedVertex)

        print(projectedVertex)

        # Seventh step: Get convex Hull
        hull = ConvexHull(projectedVertex)
