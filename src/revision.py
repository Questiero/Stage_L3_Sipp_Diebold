from formula import Formula
from MLOSolver import MLOSolver
from distanceFunction import DistanceFunction
from formulaInterpreter import FormulaInterpreter
from orOperator import Or
from andOperator import And
from unaryFormula import UnaryFormula
from nullaryFormula import NullaryFormula
from notOperator import Not
from constants import Constants
from fractions import Fraction
import math

class Revision:
    
    __solver : MLOSolver
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION):
        self.__solver = solverInit
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, onlyOneSolution)
        self._onlyOneSolution = onlyOneSolution

    def execute(self, phi : Formula, mu : Formula) -> Formula:
        phiDNF, muDNF = phi.toLessOrEqConstraint().toDNF(), mu.toLessOrEqConstraint().toDNF()
        return self.__executeDNF(self.__convertExplicit(phiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, phi: Formula, mu: Formula) -> Formula:
        
        setRes = set()
        disRes = None
        
        for miniPhi in phi.children:
            for miniMu in mu.children:
                
                lit = self.__executeLiteral(miniPhi, miniMu)
                
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
                
        return Or(formulaSet = setRes)
    
    def __executeLiteral(self, phi: Formula, mu: Formula) -> tuple[Fraction, Formula]:

        # first step: check if phi and mu are coherent
        if((not self.__interpreter.sat(phi)) or (not self.__interpreter.sat(mu))):
            return (None, mu) # None = inf
        
        # second step: find dStar
        # just for test
        dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(phi), self.__interpreter.removeNot(mu))
        
        # third step: lambdaEpsilon
        epsilon = self.__distance._epsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # fourth step: find psiPrime
        # TODO le système d'inéquations
    
        # fifth step
        if dStar % epsilon != 0:
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            return(dStar, psiPrime & mu) # TODO avec système d'inéquation
    
    def __executeConstraint(self, phi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        return self.__interpreter.optimizeCouple(phi, mu)
    
    def __convertExplicit(self, phi: Formula):
        
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
