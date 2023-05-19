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

class Revision:
    
    __solver : MLOSolver
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION):
        self.__solver = solverInit
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit)
        self._onlyOneSolution = onlyOneSolution

    def execute(self, phi : Formula, mu : Formula) -> Formula:
        phiDNF, muDNF = phi.toDNF().toLessOrEqConstraint(), mu.toDNF().toLessOrEqConstraint()
        return self.__executeDNF(self.__convertExplicit(phiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, phi: Formula, mu: Formula) -> Formula:
        
        setRes = set()
        disRes = None
        
        for miniPhi in phi.children:
            for miniMu in mu.children:
                
                lit = self.__executeLiteral(phi, mu)
                
                if (disRes is None):
                    disRes = lit[0]
                    setRes.add(lit[1])
                elif (disRes == lit[0]):
                    setRes.add(lit[1])
                elif (disRes > lit[0]):
                    disRes = lit[0]
                    setRes = {lit[1]}
                
        return Or(formulaSet = setRes)
    
    def __executeLiteral(self, phi: Formula, mu: Formula) -> tuple[Fraction, Fraction]:
        
        # first step: check if phi and mu are coherent
        if((not self.__interpreter.sat(phi)) or (not self.__interpreter.sat(mu))):
            return (Fraction("+inf"), mu) # +inf ça marche ? convention -1 ? Nouvelle classe/type ?
        
        # second step: find dStar
        dStar = self.__interpreter.optimizeCouple(self.__removeNot(phi), self.__removeNot(mu))[0]
        
        # third step: lambdaEpsilon
        pass
    
    def __executeConstraint(self, phi: Formula, mu: Formula) -> tuple[Fraction, Fraction]:
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
        
    def __removeNot(self, phi: Formula):
        
        orSet = set()
        
        for orChild in phi.children:
            
            andSet = set()
            
            for andChild in orChild:
                if isinstance(andChild, Not):
                    andSet.add(andChild.copyNeg())
                else:
                    andSet.add(andChild)
                
            orSet.add(And(formulaSet = andSet))
            
        return Or(formulaSet = orSet)