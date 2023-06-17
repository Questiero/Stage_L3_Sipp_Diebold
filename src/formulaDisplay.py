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