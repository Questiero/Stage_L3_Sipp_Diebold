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

np.set_printoptions(threshold=np.inf)

class Projector:

    __simplifier: Simplification

    """
    By default, used simplifier is a single Daalmans using lp_solve
    """
    def __init__(self, simplification: list[Simplification] = [Caron(LPSolver())]):
        self.__simplifier = simplification

    def projectOn(self, phi: And, variables: set[Variable]):

        #TODO Négation ?

        print("---")
        print(phi)
        print("---")

        constraintSet = set()

        # First step: simplify
        for simplifier in self.__simplifier:
            phi = simplifier.run(phi.toLessOrEqConstraint().toDNF())

        print(phi)
        print("---")

        # Second step: Get all variables
        allVariables = list(phi.getVariables())
        allVariables.sort(key = lambda v: v.name[::-1])
        variables = list(variables)
        variables.sort(key = lambda v: v.name[::-1])

        # Third step: Get all hyperplanes
        hyperplanes = list()

        for miniPhi in phi.children:

            hypVar = [np.array([])]

            if (isinstance(miniPhi, Not)):
                c = miniPhi.children.clone()
            else:
                c = miniPhi.clone()
            
            s = ""
            for var in allVariables:
                s += str(var) + ", "
                v = c.variables.get(var)
                if (v):
                    hypVar = np.append(hypVar, v)
                else:
                    hypVar = np.append(hypVar, Fraction(0))

            print(s)

            hyperplanes.append((hypVar, c.bound))

        for h in hyperplanes:
            print([float(a) for a in h[0]])

        # Fourth step: Get all non parallel combinations
        nonParallelCombinations = itertools.combinations(hyperplanes, len(phi.getVariables()))

#        for hyperplaneCombination in itertools.combinations(hyperplanes, len(phi.getVariables())):
#               
#            foundParallel = False
#       
#            for combinationPair in itertools.combinations(hyperplaneCombination, 2):
#       
#                x = combinationPair[0][0]
#                y = combinationPair[1][0]
#
#                #print([float(a) for a in x])
#                #print([float(a) for a in y])
#                #print(np.dot(x,y)**2)
#                #print(np.dot(x,x)*np.dot(y,y))
#                #print("-")
#       
#                if (np.dot(x,y)**2 == np.dot(x,x)*np.dot(y,y)):
#                    foundParallel = True
#                    #print("Bh")
#                    break
#        
#            if not foundParallel:
#                nonParallelCombinations.append(hyperplaneCombination)

        # Fifth step: Get all vertices from combinations
        vertices = list()

        i = 0

        for comb in nonParallelCombinations:

            a = []
            b = []

            for hyperplane in comb:
                a.append([float(x) for x in hyperplane[0]])
                b.append(float(hyperplane[1]))

            try:
                vertices.append(np.linalg.solve(a, b))
            except (np.linalg.LinAlgError):
                #print(str(i) + "Ah")
                i += 1
                continue

        vertices = np.unique(np.array(vertices), axis=0)
        print(vertices)
        print(len(vertices))

        if len(vertices) == 0:
            raise RuntimeError("Couldn't find any vertex")
        
        # Sixth step: project all vertices

        variablesBool = np.array([], dtype=bool)
        newVar = np.array([])
        for var in allVariables:
            if var in variables:
                variables = np.delete(variables, np.where(variables == var))
                newVar = np.append(newVar, var)
                variablesBool = np.append(variablesBool, True)
            else:
                variablesBool = np.append(variablesBool, False)

        projectedVertices = list()
        for v in vertices:
            projectedVertices.append(v[variablesBool])

        variables = newVar

        projectedVertices = np.array(projectedVertices)
        print(projectedVertices)

        # Seventh step: Get convex Hull
        try:
            hull = ConvexHull(projectedVertices)
        except:

            # Remove fixed dimensions

            transposed = np.transpose(projectedVertices)

            index = 0

            toRemoveIndex = []
            toRemoveVar = []

            for dim in transposed:

                foundDifferent = False

                for c in dim:
                    if not(c == dim[0]):
                        foundDifferent = True
                        break

                if not foundDifferent:

                    toRemoveIndex.append(index)
                    toRemoveVar.append(variables[index])
                    
                    lc = LinearConstraint("")
                    lc.variables[variables[index]] = Fraction(1)
                    lc.operator = ConstraintOperator.EQ
                    lc.bound = round(Fraction(dim[0]), 12)

                    constraintSet.add(lc.clone())
                
                index += 1
            
            transposed = np.delete(transposed, toRemoveIndex, axis = 0)
            variables = [i for i in variables if i not in toRemoveVar]

            projectedVertices = np.transpose(transposed)

            hull = ConvexHull(projectedVertices)

        finally:

            if projectedVertices.shape[1] == 1:

                # If project on one dimension
                max = projectedVertices[-1][0]
                min = max

                # If only one dimension, do something
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
                constraintSet.add(minLc)

                maxLc = LinearConstraint("")
                maxLc.variables[variables[0]] = Fraction(1)
                maxLc.operator = ConstraintOperator.LEQ
                maxLc.bound = round(Fraction(max), 12)
                constraintSet.add(maxLc)

            else:

                # Else, eighth step: Get constraints from hull simplices
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
                            break
                        elif(sum > lc.bound):
                            lc.operator = ConstraintOperator.GEQ
                            break
                        
                    if lc.operator is None:
                        lc.operator = ConstraintOperator.EQ

                    print(str(simplex) + ": " + str(sum) + ": " + str(lc))

                    constraintSet.add(lc)

            return And(formulaSet = constraintSet)