import formula
import solver

class Revision:
    _solver : solver.Solver

    def __init__(self, solverInit, distance):
        self._solver = solverInit

    def execute(self, phi : formula.Formula, psy : formula.Formula):
        if not self._sat(phi) or not self._sat(psy) : return psy

    def _sat(self, phi : formula.Formula):
        for constraints in phi.getConstraintGonfle():
            try:
                self._solver.solve(constraints)
                return True
            except Exception as e:
                pass
        return False