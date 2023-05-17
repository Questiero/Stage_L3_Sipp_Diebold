from formula import Formula
from MLOSolver import MLOSolver
from distanceFunction import DistanceFunction
from formulaInterpreter import FormulaInterpreter
from orOperator import Or
from andOperator import And
from unaryFormula import UnaryFormula
from nullaryFormula import NullaryFormula

class Revision:
    _solver : MLOSolver
    _distance : DistanceFunction
    _interpreter : FormulaInterpreter

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction):
        self._solver = solverInit
        self._distance = distance 
        self._interpreter = FormulaInterpreter(solverInit)

    def execute(self, phi : Formula, mu : Formula):
        phiDNF, muDNF = phi.toDNF(), mu.toDNF()
        return self.__executeDNF(self.__convertExplicit(phiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, phi: Formula, mu: Formula):
        
        setRes = set()
        
        for miniPhi in phi.children:
            for miniMu in mu.children:
                setRes.add(self.__executeLiteral(miniPhi, miniMu))
                
        return Or(formulaSet = setRes)
    
    def __executeLiteral(self, phi: Formula, mu: Formula):
        pass
    
    def __executeConstraint(self, phi: Formula, mu: Formula):
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