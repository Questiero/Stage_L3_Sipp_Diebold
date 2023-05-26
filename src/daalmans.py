from simplification import Simplification
from formula import Formula
from realVariable import RealVariable
from linearConstraint import LinearConstraint
from constraintOperator import ConstraintOperator

class Daalmans(Simplification):
    def __init__(self, solver, formulaInterpreter):
        self._solver = solver
        self._interpreter = formulaInterpreter
    
    def run(self, phi):
        return self.deleteConstraint(self.fixedVariables(phi))
    
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
                newPhi = LinearConstraint(str(var) + " = " + str(v1[2]))
                for constraint in phi.getAdherence(e)[0]:
                    constraint.replace(var,v1[2])
                    newPhi = newPhi & constraint
                phi = newPhi

        return phi

    def deleteConstraint(self, phi : Formula) -> Formula:
        e = RealVariable("@")
        phiTab = phi.getAdherence(e)[0]
        constraintUseless = []
        i = 0

        while i < len(phiTab):
            c = phiTab[i]
            if len(c.variables) == 1 and c.operator == ConstraintOperator.EQ:
                try:
                    tmpf = self.createPhi(phiTab, [i])
                    f1 = tmpf & ~LinearConstraint(str(phiTab[i]).replace('=', '<='))
                    f2 = tmpf & ~LinearConstraint(str(phiTab[i]).replace('=', '>='))
                except:
                    f1 = ~LinearConstraint(str(phiTab[i]).replace('=', '<='))
                    f2 = ~LinearConstraint(str(phiTab[i]).replace('=', '>='))
                res = self._interpreter.sat((~ (f1 | f2)).toLessOrEqConstraint().toDNF())
            else:
                try:
                    f = self.createPhi(phiTab, [i]) & ~ phiTab[i]
                except:
                    f = ~ phiTab[i]
                res = self._interpreter.sat(f.toLessOrEqConstraint().toDNF())
            if not res:
                phiTab.remove(phiTab[i])
            else:
                i += 1
        
        return self.createPhi(phiTab, [-1])

    def createPhi(self, phiTab, withoutI):
        phi = phiTab[0]
        if 0 in withoutI:
            if len(phiTab) < 2: raise Exception("Heu")
            phi = phiTab[1] 
        for i in range(0, len(phiTab)):
            if not i in withoutI:
                phi = phi & phiTab[i]

        return phi

    
    def solve(self, variables, obj, constraints):
        return self._solver.solve(variables, obj, constraints)

