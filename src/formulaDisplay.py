from .formula import Formula
from.variable import Variable
import matplotlib.pyplot as plt
import numpy as np
from .LPSolverRounded import LPSolverRounded
from .notOperator import Not
from fractions import Fraction
from .nullaryFormula import NullaryFormula
from .andOperator import And
from .orOperator import Or
import itertools
from scipy.spatial import ConvexHull
from .linearConstraint import LinearConstraint
from .constraintOperator import ConstraintOperator

class FormulaDisplay:
    def __init__(self):
        self._solver = LPSolverRounded()

    def display(self, formulas: dict[Formula, object], variables: set[Variable]):
        
        for phi in formulas.keys():
            key = phi
            phi = phi.toDNF()
            try:
                if isinstance(phi, Or):
                    for miniPhi in phi.children:
                        try:
                            self.__displayConjunction(miniPhi.toLessOrEqConstraint(), variables, formulas[key])
                        except Exception as e:
                            print("can't display : ", key)
                            print("error : ", e)
                if isinstance(phi, And):
                    self.__displayConjunction(phi.toLessOrEqConstraint(), variables, formulas[key])
                else:
                    print("Non.")
            except:
                print("can't display : ", key)

        plt.show()


    def sort_tuples_by_sum(lst):
        # create a new list of tuples where the first element is the sum of each tuple and the second element is the original tuple
        sum_tuples = [(sum(t), t) for t in lst]
        # sort the new list based on the first element (the sum)
        sorted_sum_tuples = sorted(sum_tuples, key=lambda x: x[0])
        # extract and return only the original tuples from the sorted list
        return [t[1] for t in sorted_sum_tuples]
    def __displayConjunction(self, phi: Formula, variables: set[Variable], color):

        constraintSet = set()

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

            hyperplanes.append((hypVar, c.bound))

        # Fourth step: Get all non parallel combinations
        nonParallelCombinations = itertools.combinations(hyperplanes, len(phi.getVariables()))

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

        tempVertices = []

        for vertex in vertices:

            found = False
            for miniPhi2 in phi.children:
                if (isinstance(miniPhi2, Not)):
                    constraint = miniPhi2.children.clone()
                    for var in constraint.variables.keys():
                        constraint.variables[var] *= -1
                    constraint.bound *= -1
                else:
                    constraint = miniPhi2.clone()

                sum = Fraction("0")
                for var in constraint.variables:
                    sum += constraint.variables[var] * round(Fraction(vertex[variables.index(var)]), 12)

                if sum > constraint.bound:
                    found = True
                    break

            if not found:
                tempVertices.append(vertex)

        vertices = np.array(tempVertices)

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

        projectedVertices = np.unique(np.array(projectedVertices), axis=0)
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
            if(len(projectedVertices) >= 3):
                # CA CA MARCHE QUE POUR UN TRUC QUI A 3 POINTS OU PLUS, FAIT UN CHECK ICI SUR LE NOMBRE DE PROJECTEDVERTICES JE PENSE
                test = []
                test2 = []
                for simplex in hull.simplices:
                    plt.plot(projectedVertices[simplex, 0], projectedVertices[simplex, 1], color, marker='o')
                for ver in projectedVertices[hull.vertices]:
                    test.append(ver[0])
                    test2.append(ver[1])

                plt.fill(test, test2, color, alpha=0.3)
            elif(len(projectedVertices) == 2) :
                    test = [[projectedVertices[0][0], projectedVertices[1][0]], [projectedVertices[0][1], projectedVertices[1][1]]]
                    plt.plot(test[0],test[1], color=color, marker='o')
                    plt.plot(test[0],test[1], color=color)
            elif(len(projectedVertices) == 1):
                plt.plot([vertex[0]], [vertex[1]], color=color, marker='o')