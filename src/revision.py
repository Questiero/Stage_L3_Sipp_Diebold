import formula
import MLOSolver
import distanceFunction
import formulaInterpreter
import orOperator

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
        return self.__executeDNF(phiDNF, muDNF)
        
    def __executeDNF(self, phi: formula.Formula, mu: formula.Formula):
        
        formulaRes = orOperator.Or()
        
        for miniPhi in phi.children:
            for miniMu in mu.children:
                formulaRes.children.append(self.__executeLiteral(miniPhi, miniMu))
        
        return formulaRes
    
    def __executeLiteral(self, phi: formula.Formula, mu: formula.Formula):
        pass