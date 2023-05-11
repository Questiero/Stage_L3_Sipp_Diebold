import formula
import MLOSolver
import distanceFunction
import formulaInterpreter

class Revision:
    _solver : MLOSolver.MLOSolver
    _distance : distanceFunction.DistanceFunction
    _interpreter : formulaInterpreter.FormulaInterpreter

    def __init__(self, solverInit : MLOSolver.MLOSolver, distance : distanceFunction.DistanceFunction):
        self._solver = solverInit
        self._distance = distance 
        self._interpreter = formulaInterpreter.FormulaInterpreter(solverInit)

    def execute(self, phi : formula.Formula, psy : formula.Formula):
        return self._interpreter.sat(phi)
        #if not self._interpreter.sat(phi) or not self._interpreter.sat(psy) : return psy