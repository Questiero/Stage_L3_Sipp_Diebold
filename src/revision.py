from formula import Formula
from MLOSolver import MLOSolver
from distanceFunction import DistanceFunction
from formulaInterpreter import FormulaInterpreter
from orOperator import Or
from andOperator import And
from unaryFormula import UnaryFormula
from nullaryFormula import NullaryFormula
from linearConstraint import LinearConstraint
from notOperator import Not
from constants import Constants
from fractions import Fraction
from simplification import Simplification
from projector import Projector
import math

class Revision:
    
    __solver : MLOSolver
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    __projector : Projector
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifier : Simplification = None, onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION):
        self.__solver = solverInit
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, simplifier, onlyOneSolution)
        self._onlyOneSolution = onlyOneSolution
        self.__projector = Projector(simplifier)

    def execute(self, psi : Formula, mu : Formula) -> Formula:
        psiDNF, muDNF = psi.toLessOrEqConstraint().toDNF(), mu.toLessOrEqConstraint().toDNF()
        return self.__executeDNF(self.__convertExplicit(psiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, psi: Formula, mu: Formula) -> Formula:
        
        setRes = set()
        disRes = None
        
        for minipsi in psi.children:
            for miniMu in mu.children:
                
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
                
        return self.__interpreter.simplifyMLC(Or(formulaSet = setRes).toDNF())
    
    def __executeLiteral(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:

        # first step: check if phi and mu are coherent
        if((not self.__interpreter.sat(psi)) or (not self.__interpreter.sat(mu))):
            return (None, mu) # None = inf
        
        # second step: find dStar
        # just for test
        dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(psi), self.__interpreter.removeNot(mu))
        
        # third step: lambdaEpsilon
        epsilon = self.__distance._epsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # fourth step: find psiPrime
        # psiPrime = self.__project(psi, lambdaEpsilon)
    
        # fifth step
        if dStar % epsilon != 0:
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            # lambdaEpsilon = dStar + epsilon
            # psiPrime = self.__project(psi, lambdaEpsilon)
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

    def __project(self, psi: And, lambdaEpsilon: Fraction) -> Formula:
        
        yVariables = {v: v.declareAnonymous() for v in psi.getVariables()}

        constraintSet = set()

        # Create x in M(psi) constraints and change variables
        for minipsi in psi.children:
            if isinstance(minipsi, Not):
                const = minipsi.children.clone()
                for key in const.variables:
                    const[yVariables[key]] = const[key]
                    del const[key]
                constraintSet.add(Not(const))
            else:
                const = minipsi.clone()
                for key in const.variables:
                    const[yVariables[key]] = const[key]
                    del const[key]
                constraintSet.add(const)

        # Add distance function constraints
        zVariables = {v: v.declareAnonymous() for v in psi.getVariables()}
        for yVar in yVariables:
            z = zVariables[yVar]
            # Creating link between x, y and z
            const = LinearConstraint(yVar.name + "<= 0")
            const.variables[yVariables[yVar]] = 1
            const.variables[z] = -1
            constraintSet.add(const)
            const = LinearConstraint(yVar.name + ">= 0")
            const.variables[yVariables[yVar]] = 1
            const.variables[z] = -1
            constraintSet.add(const)
            # Keeping z in memory
            zVariables[yVar] = z

        # TODO pas sûr de mon code, à tester
        # Generate distance constraint
        tempZ = zVariables.popitem()
        distanceConstraint = LinearConstraint(tempZ[0] + " <= " + str(lambdaEpsilon))
        distanceConstraint.variables[tempZ[1]] = self.__distance.getWeights()[tempZ[0]]
        del distanceConstraint.variables[tempZ[0]]
        for z in zVariables:
            distanceConstraint.variables[z] = self.__distance.getWeights()[z]
        constraintSet.add(distanceConstraint)

        return self.__projector.projectOn(And(formulaSet = constraintSet), yVariables.keys())