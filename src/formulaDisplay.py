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

    def draw(self, formulas : dict[Formula, object], variables : tuple[Variable, Variable]) -> None :

        d = np.linspace(0,7,300)
        for phi in formulas.keys():
            key = phi
            if isinstance(phi, NullaryFormula): phi = And(phi)
            if isinstance(phi, And): phi = Or(phi)
            for orChild in phi.children:
                x,y = np.meshgrid(d,d)
                polygone = None
                for miniPhi in orChild.children:
                    if variables[0] in miniPhi.variables or variables[1] in miniPhi.variables:
                        if isinstance(polygone, None.__class__) : 
                            polygone = (x*(miniPhi.variables[variables[0]] if  variables[0] in miniPhi.variables else 0)+ y*(miniPhi.variables[variables[1]] if  variables[1] in miniPhi.variables else 0) <= miniPhi.bound)
                        else : polygone = polygone & (x*(miniPhi.variables[variables[0]] if  variables[0] in miniPhi.variables else 0)+ y*(miniPhi.variables[variables[1]] if  variables[1] in miniPhi.variables else 0) <= miniPhi.bound)
                plt.imshow( (polygone).astype(int) , extent=(x.min(),x.max(),y.min(),y.max()),origin="lower", cmap=formulas[key], alpha = 0.3)
        plt.show()

    def display(self, formulas : dict[Formula, object], variablesParam : tuple[Variable, Variable]) -> None :
        fig, ax = plt.subplots()
        ax.set_xlim([0,7])
        ax.set_ylim([0,7])
        for orPhi in formulas.keys(): 
            key = orPhi
            if isinstance(orPhi, NullaryFormula): orPhi = And(orPhi)
            if isinstance(orPhi, And): orPhi = Or(orPhi)
            for phi in orPhi.children:
                #TODO Négation ?

                constraintSet = set()

                # Second step: Get all variables
                allVariables = list(phi.getVariables())
                variables = list(allVariables)

                # Third step: Get all hyperplanes
                hyperplanes = list()
                points = []

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

                variables = list(newVar)

                projectedVertices = np.array(projectedVertices)
                res = []
                for vertex in projectedVertices:
                    mustBeSaved = True
                    for constraint in phi.children:
                        if mustBeSaved:
                            mustBeSaved = mustBeSaved and (vertex[1 if variables.index(variablesParam[0]) == 1 else 0] * (0 if not variablesParam[0] in constraint.variables else constraint.variables[variablesParam[0]]) + vertex[1 if variables.index(variablesParam[1]) == 1 else 0] * (0 if not variablesParam[1] in constraint.variables else constraint.variables[variablesParam[1]]) <= constraint.bound)
                    if mustBeSaved : res.append(vertex)
                points += res
                print(phi)
                print(points)
                for vertex in points:
                    ax.scatter(vertex[1 if variables.index(variablesParam[0]) == 1 else 0],vertex[1 if variables.index(variablesParam[1]) == 1 else 0], color = formulas[key])
                from matplotlib.patches import Polygon
                points.append(points[0])
                p = Polygon(points, color=formulas[key])
                ax.add_patch(p)

        plt.show()
                    
    def displayv2(self, formulas : dict[Formula, object], variablesParam : tuple[Variable, Variable]) -> None :
        
        fig, ax = plt.subplots()
        ax.set_xlim([0,7])
        ax.set_ylim([0,7])

        variables = set()

        for orPhi in formulas.keys():
            # Second step: Get all variables
            allVariables = orPhi.getVariables()
            variables = set(variables) | allVariables
        variablesList = list(variables)
        variablesList.sort(key = lambda v: v.name[::-1])
        for orPhi in formulas.keys(): 
            key = orPhi
            if isinstance(orPhi, NullaryFormula): orPhi = And(orPhi)
            if isinstance(orPhi, And): orPhi = Or(orPhi)
            for phi in orPhi.children:
                constraintSet = set()
                points = []

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

                # Seventh step: Get convex Hull
                try:
                    hull = ConvexHull(projectedVertices)
                    print(1)
                except:
                    print(2)
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

                    try:
                        hull = ConvexHull(projectedVertices)
                    except:
                        valx = 0
                        valy = 0
                        for c in phi.children:
                            valx += c.variables[variablesParam[0]] if variablesParam[0] in c.variables else 0
                            valy += c.variables[variablesParam[1]] if variablesParam[1] in c.variables else 0
                        if variablesList.index(variablesParam[0]) == 1 :
                            valx, valy = valy, valx
                        points.append([valx , valy])

                finally:

                    if projectedVertices.shape[1] == 1:

                        # If project on one dimension
                        max = projectedVertices[-1][0]
                        min = max

                        # If only one dimension, do something
                        for vertex in projectedVertices:
                            points.append(vertex)
            for vertex in points:
                    ax.scatter(vertex[1 if variablesList.index(variablesParam[0]) == 1 else 0],vertex[1 if variablesList.index(variablesParam[1]) == 1 else 0], color = formulas[key])
            
            from matplotlib.patches import Polygon
            try:
                points.append(points[0])
                p = Polygon(points, color=formulas[key])
                ax.add_patch(p)  
            except: pass
       
        plt.show()

    def displayv3(self, formulas: dict[Formula, object], variables: set[Variable]):
        
        for phi in formulas.keys():
            key = phi
            phi = phi.toDNF()
            try:
                if isinstance(phi, Or):
                    for miniPhi in phi.children:
                        try:
                            self.__displayConjunction(miniPhi.toLessOrEqConstraint(), variables, formulas[key])
                        except:
                            print("can't display : ", key)
                if isinstance(phi, And):
                    self.__displayConjunction(phi.toLessOrEqConstraint(), variables, formulas[key])
                else:
                    print("Non.")
            except:
                print("can't display : ", key)

        plt.show()

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
            for miniPhi in phi.children:

                sum = Fraction("0")
                for var in miniPhi.variables:
                    sum += miniPhi.variables[var] * round(Fraction(vertex[variables.index(var)]), 12)

                if sum > miniPhi.bound:
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
                for simplex in hull.simplices:
                    plt.plot(projectedVertices[simplex, 0], projectedVertices[simplex, 1], color)
            elif(len(projectedVertices) == 2) :
                    test = [[projectedVertices[0][0], projectedVertices[1][0]], [projectedVertices[0][1], projectedVertices[1][1]]]
                    plt.plot(test[0],test[1], color=color, marker='o')
                    plt.plot(test[0],test[1], color=color)
            elif(len(projectedVertices) == 1):
                pass #TO DO
