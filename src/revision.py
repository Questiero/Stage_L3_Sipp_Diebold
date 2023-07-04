r"""
Main class of the module, allowing the user to make the knowledge revision between two `src.formula.formula.Formula`
\(\psi\) and \(\mu\) that are mixed integer linear constraints.
"""

from __future__ import annotations

from .formula import Formula, Or, And, UnaryFormula, NullaryFormula, LinearConstraint, Not, ConstraintOperator
from .formulaInterpreter import FormulaInterpreter
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector

from fractions import Fraction
import math

class Revision:
    r"""
    Main class of the module, allowing the user to make the knowledge revision between two `src.formula.formula.Formula`
    \(\psi\) and \(\mu\) that are mixed integer linear constraints.

    Parameters
    ----------
    solverInit : `src.mlo_solver.MLOSolver.MLOSolver`
        The solver that will be used for optimization.
    distance : `src.distance.distance_function.distanceFunction.DistanceFunction`
        The distance function that will be used and, more importantly, the weights \((w_i)\) and \(\varepsilon\) arguments of it.
        The original algorithm is meant to be used with a `src.distance.distance_function.discreteL1DistanceFunction.discreteL1DistanceFunction`.
    simplifiers : list of `src.simplificator.simplificator.Simplificator`, optional
        List of all of the `src.simplificator.simplificator.Simplificator` that will be applied to the `src.formula.formula.Formula`, 
        in order given by the list.
    onlyOneSolution : boolean, optional
        If set to `True`, the revision algorithm will by default only return one point that satisfies \(\psi \circ \mu\).
        If not, it will return all solutions.
        By default, this constant is set to whichever one was chosen in `src.constants.Constants`.
    """
    
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    __projector : Projector
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, projector: Projector = None) -> None:        
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, simplifiers)
        self._onlyOneSolution = onlyOneSolution

        self.__projector = projector

    def execute(self, psi : Formula, mu : Formula) -> tuple[Fraction, Formula]:
        r"""
        Execute the revision of \(\psi\) by \(\mu\).

        Parameters
        ----------
        psi : `src.formula.formula.Formula`
            \(\psi\), left part of the knowledge revision operator and `src.formula.formula.Formula` that will be revised.
        mu : `src.formula.formula.Formula`
            \(\mu\), right part of the knowledge revision operator and `src.formula.formula.Formula` that will be used to revise \(\psi\) by.


        Returns
        -------
        Fraction
            Distance (calculated with the `src.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) between \(\psi\) and \(\mu\).
        `src.formula.formula.Formula`
            Result of the knowledge revison of \(\psi\) by \(\mu\).
        """

        psiDNF, muDNF = psi.toLessOrEqConstraint().toDNF(), mu.toLessOrEqConstraint().toDNF()
        return self.__executeDNF(self.__convertExplicit(psiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        
        res = None
        disRes = None

        if(self._onlyOneSolution):
            
            for minipsi in psi.children:
                for miniMu in mu.children:
                    
                    lit = self.__executeLiteral(minipsi, miniMu)

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

        else:

            setRes = set()
            
            for minipsi in psi.children:
                for miniMu in mu.children:
                    
                    lit = self.__executeLiteral(minipsi, miniMu)
                    #print("---")
                    #print(str(lit[0]) + "; " + str(lit[1]))
                    
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
            
            res = Or(formulaSet = setRes).toDNF()

        return (disRes, self.__interpreter.simplifyMLC(res.toLessOrEqConstraint().toDNF()))
    
    def __executeLiteral(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:

        # first step: check if psi and mu are coherent
        if((not self.__interpreter.sat(psi)) or (not self.__interpreter.sat(mu))):
            return (None, mu) # None = inf
        
        # second step: find dStar (and psiPrime if onlyOneSoltuion)
        dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(psi), self.__interpreter.removeNot(mu))

        # third step: lambdaEpsilon
        epsilon = self.__distance._epsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # fourth step: find psiPrime (only if not onlyOneSolution)
        if(not self._onlyOneSolution):
            psiPrime = self.__expand(psi, lambdaEpsilon)
    
        # fifth step
        if dStar % epsilon != 0:
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            lambdaEpsilon = dStar + epsilon
            psiPrime = self.__expand(psi, lambdaEpsilon)
            return(dStar, psiPrime & mu)
    
    def __executeConstraint(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        return self.__interpreter.optimizeCouple(psi, mu)
    
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
            return Or(formulaSet = orSet)

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

        return self.__projector.projectOn(And(formulaSet = set(constraints)), yVariables.keys())

        #try:
        #    return self.__projector.projectOn(And(formulaSet = set(constraints)), yVariables.keys())
        #except RuntimeError:
        #    if isinstance(psi, NaryFormula):
        #        return And(formulaSet = {self.__expandLiteral(c, lambdaEpsilon) for c in psi.children})
        #    else:
        #        return self.__expandLiteral(psi, lambdaEpsilon)

    def __expandLiteral(self, psi: Formula, lambdaEpsilon: Fraction):
        
        if isinstance(psi, Not):

            lc = psi.children.clone()
            
            match lc.operator:
                case ConstraintOperator.LEQ:
                    lc.bound += lambdaEpsilon
                case ConstraintOperator.GEQ:
                    lc.bound -= lambdaEpsilon
                case ConstraintOperator.EQ:
                    return And(formulaSet = {Not(self.__expandLiteral(c)) for c in psi.toLessOrEqConstraint().children})

            return Not(lc)

        else:

            lc = psi.clone()

            match lc.operator:
                case ConstraintOperator.LEQ:
                    lc.bound += lambdaEpsilon
                case ConstraintOperator.GEQ:
                    lc.bound -= lambdaEpsilon
                case ConstraintOperator.EQ:
                    return And(formulaSet = {self.__expandLiteral(c) for c in psi.toLessOrEqConstraint().children})

            return lc