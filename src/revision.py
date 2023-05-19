from formula import Formula
from MLOSolver import MLOSolver
from distanceFunction import DistanceFunction
from formulaInterpreter import FormulaInterpreter
from orOperator import Or
from andOperator import And
from unaryFormula import UnaryFormula
from nullaryFormula import NullaryFormula
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
        phiDNF, muDNF = phi.toDNF(), mu.toDNF()
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
        pass
    
    def __executeConstraint(self, phi: Formula, mu: Formula) -> tuple[Fraction, Fraction]:
        pass
    
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