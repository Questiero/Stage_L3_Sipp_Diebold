from .andOperator import And
from .simplification import Simplification
from .caron import Caron
from .LPSolver import LPSolver
from .linearConstraint import LinearConstraint
from .notOperator import Not
from .constraintOperator import ConstraintOperator

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
    def __init__(self, simplification: list[Simplification] = [Caron(LPSolver())]):
        self.__simplifier = simplification

    def projectOn(self, phi: And, variables: set[Variable]):

        #TODO Négation ?

        # First step: simplify
        for simplifier in self.__simplifier:
            phi = simplifier.run(phi)

        # Second step: Get all variables
        allVariables = list(phi.getVariables())
        variables = list(variables)

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

#       for hyperplaneCombination in itertools.combinations(hyperplanes, len(phi.getVariables())):
#               
#           foundParallel = False
#       
#           for combinationPair in itertools.combinations(hyperplaneCombination, 2):
#       
#               x = combinationPair[0][0]
#               y = combinationPair[1][0]
#       
#               if (np.dot(x,y)*np.dot(x,y) == np.dot(x,x)*np.dot(y,y)):
#                   foundParallel = True
#                   break
#       
#           if not foundParallel:
#               nonParallelCombinations.append(hyperplaneCombination)

        # Fifth step: Get all vertices from combinations
        vertices = list()

        for comb in nonParallelCombinations:
            a = []
            b = []
            for hyperplane in comb:
                a.append([float(x) for x in hyperplane[0]])
                b.append(float(hyperplane[1]))

            try:
                vertices.append(np.linalg.solve(a, b))    
            except (np.linalg.LinAlgError):
                pass

        vertices = np.array(vertices)
        
        # Sixth step: project all vertices
        variablesBool = np.array([], dtype=bool)
        for var in allVariables:
            if var in variables:
                variablesBool = np.append(variablesBool, True)
            else:
                variablesBool = np.append(variablesBool, False)

        projectedVertices = list()
        for v in vertices:
            projectedVertices.append(v[variablesBool])

        projectedVertices = np.array(projectedVertices)

        # Seventh step: Get convex Hull
        try:
            hull = ConvexHull(projectedVertices)
        except:
            
            # If project on one dimension
            max, projectedVertices = projectedVertices[-1][0], projectedVertices[:-1]
            min = max

            for vertex in projectedVertices:
                val = vertex[0]
                if val >= max:
                    max = val
                elif val <= min:
                    min = val
                
            minLc = LinearConstraint("")
            minLc.variables[variables[0]] = Fraction(1)
            minLc.operator = ConstraintOperator.GEQ
            minLc.bound = round(Fraction(min), 12)

            maxLc = LinearConstraint("")
            maxLc.variables[variables[0]] = Fraction(1)
            maxLc.operator = ConstraintOperator.LEQ
            maxLc.bound = round(Fraction(max), 12)

            constraintSet = {minLc, maxLc}

        else:
            # Eighth step: Get constraints from hull simplices
            constraintSet = set()
            for simplex in hull.simplices:

                # Get centroid and normal
                points = projectedVertices[simplex]
                centroid = np.mean(points, axis=0)
                u, s, vh = np.linalg.svd(points - centroid, full_matrices=False)
                normal = vh[-1]
                normal = normal * np.linalg.norm(normal, 1)
                
                # Build constraint
                lc = LinearConstraint("")
                for i in range(len(normal)):
                    if normal[i] != 0:
                        lc.variables[variables[i]] = round(Fraction(normal[i]), 12)
                lc.bound = round(Fraction(np.sum(normal * centroid)), 12)

                for vertex in projectedVertices:

                    sum = Fraction("0")
                    for i in range(len(variables)):
                        coef = lc.variables.get(variables[i])
                        if coef:
                            sum += vertex[i]*coef
                    if(sum < lc.bound):
                        lc.operator = ConstraintOperator.LEQ
                    elif(sum > lc.bound):
                        lc.operator = ConstraintOperator.GEQ
                    else:
                        lc.operator = ConstraintOperator.EQ

                constraintSet.add(lc)
        finally:
            return And(formulaSet = constraintSet)