import formula
import MLOSolver
import distanceFunction
import formulaInterpreter
import orOperator
import andOperator
import unaryFormula
import nullaryFormula

class Revision:
    _solver : MLOSolver.MLOSolver
    _distance : distanceFunction.DistanceFunction
    _interpreter : formulaInterpreter.FormulaInterpreter

    def __init__(self, solverInit : MLOSolver.MLOSolver, distance : distanceFunction.DistanceFunction):
        self._solver = solverInit
        self._distance = distance 
        self._interpreter = formulaInterpreter.FormulaInterpreter(solverInit)

    def execute(self, phi : formula.Formula, mu : formula.Formula):
        phiDNF, muDNF = phi.toDNF(), mu.toDNF()
        return self.__executeDNF(self.__convertExplicit(phiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, phi: formula.Formula, mu: formula.Formula):
        
        setRes = set()
        
        for miniPhi in phi.children:
            for miniMu in mu.children:
                setRes.add(self.__executeLiteral(miniPhi, miniMu))
                
        return orOperator.Or(formulaSet = setRes)
    
    def __executeLiteral(self, phi: formula.Formula, mu: formula.Formula):
        pass
    
    def __executeConstraint(self, phi: formula.Formula, mu: formula.Formula):
        pass
    
    def __convertExplicit(self, phi: formula.Formula):
        
        if isinstance(phi, andOperator.And):
            return orOperator.Or(phi)
        elif isinstance(phi, unaryFormula.UnaryFormula) | isinstance(phi, nullaryFormula.NullaryFormula):
            return orOperator.Or(andOperator.And(phi))
        else:
            orSet = set()
            for miniPhi in phi.children:
                if isinstance(miniPhi, andOperator.And):
                    orSet.add(miniPhi)
                else:
                    orSet.add(andOperator.And(miniPhi))
            return orOperator.Or(formulaSet = orSet)