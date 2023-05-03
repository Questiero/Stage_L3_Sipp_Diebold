from formula.Formula import *
from solver.Solver import *

class Revision:
    _solver : Solver

    def __init__(self, solver, distance):
        self._solver = solver

    def execute(self, phi : Formula, psy : Formula):
        if not self._sat(phi) or not self._sat(psy) : return psy

    def _sat(self, phi : Formula):
        for constraints in phi.getConstraintGonfle():
            try:
                self._solver.solve(constraints)
                return True
            except Exception as e:
                pass
        return False