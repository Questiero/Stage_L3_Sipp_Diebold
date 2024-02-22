r"""
Main class of the module, allowing the user to make the knowledge revision between two `src.formula.formula.Formula`
\(\psi\) and \(\mu\) that are mixed integer linear constraints.
"""

from __future__ import annotations

from .formula import Formula, Or, And, UnaryFormula, NullaryFormula, LinearConstraint, Not, ConstraintOperator, PropositionalVariable
from .formulaInterpreter import FormulaInterpreter
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .variable import IntegerVariable, RealVariable

from fractions import Fraction
from tqdm import tqdm
import time

import math

class Revision:
    r"""
    Main class of the module, allowing the user to make the knowledge revision between two `src.formula.formula.Formula`
    \(\psi\) and \(\mu\) that are mixed integer linear constraints.

    Parameters
    ----------
    solverInit : src.mlo_solver.MLOSolver.MLOSolver
        The solver that will be used for optimization.
    distance : src.distance.distance_function.distanceFunction.DistanceFunction
        The distance function that will be used and, more importantly, the weights \((w_i)\) and \(\varepsilon\) arguments of it.
        The original algorithm is meant to be used with a `src.distance.distance_function.discreteL1DistanceFunction.discreteL1DistanceFunction`.
    simplifiers : list of src.simplificator.simplificator.Simplificator, optional
        List of all of the `src.simplificator.simplificator.Simplificator` that will be applied to the `src.formula.formula.Formula`, 
        in order given by the list.
    onlyOneSolution : boolean, optional
        If set to `True`, the revision algorithm will by default only return one point that satisfies \(\psi \circ \mu\).
        If not, it will return all solutions.
        By default, this constant is set to whichever one was chosen in `src.constants.Constants`.
    """
    
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, projector: Projector = None) -> None:        
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, simplifiers)
        self._onlyOneSolution = onlyOneSolution

        self.__projector = projector

    def execute(self, psi : Formula, mu : Formula, propToInt : dict[PropositionalVariable, IntegerVariable] = None) -> tuple[Fraction, Formula]:
        r"""
        Execute the revision of \(\psi\) by \(\mu\).

        Parameters
        ----------
        psi : src.formula.formula.Formula
            \(\psi\), left part of the knowledge revision operator and `src.formula.formula.Formula` that will be revised.
        mu : src.formula.formula.Formula
            \(\mu\), right part of the knowledge revision operator and `src.formula.formula.Formula` that will be used to revise \(\psi\) by.


        Returns
        -------
        Fraction
            Distance (calculated with the `src.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) between \(\psi\) and \(\mu\).
        src.formula.formula.Formula
            Result of the knowledge revison of \(\psi\) by \(\mu\).
        """

        self.__timeStart = time.perf_counter()

        if propToInt is None:
            propToInt = dict()

        weights = self.__distance.getWeights()

        for var in weights.copy().keys():
            if isinstance(var, PropositionalVariable):

                if propToInt.get(var) is None:
                    tempVar = IntegerVariable.declareAnonymous("e_" + var.nameVariable)
                    propToInt[var] = tempVar

                intVar = propToInt[var]

                weights[intVar] = weights[var]

        print("")
        print(self.getTime(), "Transforming Psi in DNF form")
        psiDNF = psi.toPCMLC(propToInt).toLessOrEqConstraint().toDNF()

        print("")
        print(self.getTime(), "Transforming Mu in DNF form")
        muDNF = mu.toPCMLC(propToInt).toLessOrEqConstraint().toDNF()

        res = self.__executeDNF(self.__convertExplicit(psiDNF), self.__convertExplicit(muDNF))

        print("")
        print(self.getTime(), f"Solution found with distance of {res[0]}:")
        print(res[1])
        print("")

        return res
        
    def __executeDNF(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        
        res = None
        disRes = None

        print("")
        satPsi = set()
        for miniPsi in tqdm(psi.children, desc=f"{self.getTime()} Testing satisfiability of each child of Psi", mininterval=0.5):
            if self.__interpreter.sat(miniPsi):
                satPsi.add(miniPsi)

        if len(satPsi) == 0:
            raise(AttributeError("Psi is not satisfiable"))

        print(self.getTime(), f"{len(satPsi)} satisfiable children of Psi found")

        print("")
        satMu = set()
        for miniMu in tqdm(mu.children, desc=f"{self.getTime()} Testing satisfiability of each child of Mu", mininterval=0.5):
            if self.__interpreter.sat(miniMu):
                satMu.add(miniMu)

        if len(satMu) == 0:
            raise(AttributeError("Mu is not satisfiable"))

        print(self.getTime(), f"{len(satMu)} satisfiable children of Psi found")

        maxIter = len(satPsi)*len(satMu)
        print("")
        print(self.getTime(), f"{maxIter} combinations of conjunctions found")

        if(self._onlyOneSolution):
            
            with tqdm(total=maxIter, desc=f"{self.getTime()} Revision of each combination", mininterval=0.5) as pbar:
                for minipsi in satPsi:
                    for miniMu in satMu:
                    
                        lit = self.__executeLiteral(minipsi, miniMu)

                        if self.__interpreter.sat(lit[1]):
                            if not (lit[0] is None):
                                if (disRes is None):
                                    disRes = lit[0]
                                    res = lit[1]
                                elif (disRes > lit[0]):
                                    disRes = lit[0]
                                    res = lit[1]
                            else:
                                if (disRes is None) & (res is None):
                                    res = lit[1]

                        pbar.update(1)

        else:

            setRes = set()
            
            with tqdm(total=maxIter, desc="Revision of each combination", mininterval=0.5) as pbar:
                for minipsi in satPsi:
                    for miniMu in satMu:
                                            
                        lit = self.__executeLiteral(minipsi, miniMu)
                        
                        if not (lit[0] is None):
                            if (disRes is None):
                                disRes = lit[0]
                                setRes = {lit[1]}
                            elif (disRes == lit[0]):
                                setRes.add(lit[1])
                            elif (disRes > lit[0]):
                                disRes = lit[0]
                                setRes = {lit[1]}
                        else:
                            if (disRes is None):
                                setRes.add(lit[1])

                        pbar.update(1)
            
            res = Or(*setRes).toDNF()

        return (disRes, self.__interpreter.simplifyMLC(res.toLessOrEqConstraint().toDNF()))
    
    def __executeLiteral(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        
        epsilon = self.__distance._epsilon

        # second step: find dStar (and psiPrime if onlyOneSoltuion)
        dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(psi), self.__interpreter.removeNot(mu))

        # third step: lambdaEpsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # print(lambdaEpsilon, psiPrime)
        # fourth step: find psiPrime (only if not onlyOneSolution)
        if(not self._onlyOneSolution):
            psiPrime = self.__expand(psi, lambdaEpsilon)
    
        # fifth step
        if dStar % epsilon != 0:
            # print("dStar % epsilon != 0")
            if self._onlyOneSolution & (not self.__interpreter.sat(psiPrime & mu)):
                psiPrime = self.__interpreter.optimizeCoupleWithLimit(self.__interpreter.removeNot(psi, epsilon), self.__interpreter.removeNot(mu, epsilon), lambdaEpsilon)[1]
            # print("psiPrime2:", psiPrime)
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            # print("else")
            lambdaEpsilon = dStar + epsilon
            if (self._onlyOneSolution):
                psiPrime = self.__interpreter.optimizeCoupleWithLimit(self.__interpreter.removeNot(psi, epsilon), self.__interpreter.removeNot(mu, epsilon), lambdaEpsilon)[1]
            else:
                psiPrime = self.__expand(psi, lambdaEpsilon)
            # print("psiPrime2:", psiPrime)
            return(dStar, psiPrime & mu)
    
    def __executeConstraint(self, phi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        return self.__interpreter.optimizeCouple(phi, mu)
    
    def __convertExplicit(self, phi: Formula) -> Formula:
        
        if isinstance(phi, And):
            return Or(phi)
        elif isinstance(phi, UnaryFormula) | isinstance(phi, NullaryFormula):
            return Or(And(phi))
        else:
            orSet = set()
            for miniPhi in phi.children:
                if isinstance(miniPhi, And):
                    orSet.add(miniPhi)
                else:
                    orSet.add(And(miniPhi))
            return Or(*orSet)

    def __expand(self, psi: Formula, lambdaEpsilon: Fraction) -> Formula:
        
        yVariables = {v: v.__class__.declareAnonymous(ending = ("y" + str(v.name))) for v in psi.getVariables()}

        constraints = list()

        # Create x in M(psi) constraints and change variables
        for minipsi in psi.children:
            if isinstance(minipsi, Not):
                const = minipsi.children.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(Not(const))
            else:
                const = minipsi.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(const)

        # Add distance function constraints
        zVariables = {v: v.__class__.declareAnonymous(ending = ("z" + str(v.name))) for v in psi.getVariables()}
        for yVar in yVariables:
            z = zVariables[yVar]
            # Creating link between x, y and z
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(-1)
            const.variables[yVariables[yVar]] = Fraction(1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(1)
            const.variables[yVariables[yVar]] = Fraction(-1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            # Keeping z in memory
            zVariables[yVar] = z

        # TODO pas sûr de mon code, à tester
        # TODO fonction de distance, les poids ?
        # Generate distance constraint
        distanceConstraint = LinearConstraint("")
        distanceConstraint.operator = ConstraintOperator.LEQ
        distanceConstraint.bound = lambdaEpsilon
        for z in zVariables:
            distanceConstraint.variables[zVariables[z]] = self.__distance.getWeights()[z]
        constraints.append(distanceConstraint)

        expandConstraint = And(*constraints)

        return self.__projector.projectOn(expandConstraint, yVariables.keys())
    
    def getTime(self):
        return f"{int((time.perf_counter()-self.__timeStart)//60)}m{(time.perf_counter()-self.__timeStart)%60:0.3f}s"