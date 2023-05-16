import formula
import MLOSolver
import realVariable
import unaryFormula
import orOperator
import constraintOperator

class FormulaInterpreter:
    def __init__(self, mloSolver : MLOSolver.MLOSolver) -> None:
        self.MLOSolver = mloSolver

    def __interpretFormula(self, phi : formula.Formula):
        variables = list(phi.getVariables())
        variables.append(realVariable.RealVariable("@"))




    def sat(self, phi : formula.Formula) -> bool:
        variables = list(phi.getVariables())
        e = realVariable.RealVariable("@")
        variables.append(e)

        for lc in phi.getAdherence(e):
            res = self.MLOSolver.solve(variables, list(map(lambda v : -1 if v == e else 0, variables)), lc)
            if res[0] :
                if res[1][variables.index(e)] != 0:
                    return True
            
        return False
