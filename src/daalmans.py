from simplification import Simplification
from formula import Formula
from realVariable import RealVariable
from linearConstraint import LinearConstraint

class Daalmans(Simplification):
    def __init__(self, solver, formulaInterpreter):
        self._solver = solver
        self._interpreter = formulaInterpreter
    
    def run(self, phi):
        return self.fixedVariables(phi)
    
    def fixedVariables(self, phi : Formula) -> Formula:
        variables = list(phi.getVariables())
        variablesWithE = variables
        e = RealVariable("@")
        variablesWithE.append(e)

        for var in variables:
            tabPhi = self.toTab(phi,e)
            obj = []
            for var2 in variablesWithE:
                if var == var2: obj.append(1)
                else: obj.append(0)
            v1 = self.solve(variablesWithE, obj, tabPhi)
            for i in range(0, len(obj)) : obj[i] *= -1
            v2 = self.solve(variablesWithE, obj, tabPhi)

            if v1[0] and v2[0] and v1[1][variables.index(var)] == v2[1][variables.index(var)] :
                phi = phi & LinearConstraint(str(var) + " = " + str(v1[2]))
                
        return phi

    
    def solve(self, variables, obj, constraints):
        return self._solver.solve(variables, obj, constraints)

