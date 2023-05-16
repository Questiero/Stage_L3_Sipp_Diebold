import formula
import MLOSolver
import realVariable
import constraint

class FormulaInterpreter:
    def __init__(self, mloSolver : MLOSolver.MLOSolver) -> None:
        self.MLOSolver = mloSolver

    def simplifyMLC(self, phi : formula.Formula):
        '''
        Method used to simplify a conjonction of mix linears constraints

        Attributes
        ----------
        phi : the formula to simplify

        Returns
        -------
        res: the formula with mlc simplified
        '''
        return phi

    def sat(self, phi : formula.Formula) -> bool:
        '''
        Method used to verify the satisfiability of a formula

        Attributes
        ----------
        phi : the formula

        Returns
        -------
        res: true if the formula is satsifiable, false in the other case
        
        '''
        variables = list(phi.getVariables())
        e = realVariable.RealVariable("@")
        variables.append(e)

        for lc in phi.getAdherence(e):
            res = self.MLOSolver.solve(variables, list(map(lambda v : -1 if v == e else 0, variables)), lc)
            if res[0] :
                if res[1][variables.index(e)] != 0:
                    return True
            
        return False

    def findAllSolutions(self, x) -> tuple[float, formula.Formula]:
        pass

    def findOneSolution(self, x) -> tuple[float, formula.Formula]:
        pass

    def revisionOnLitteral(self, phi : constraint.Constraint, mu : constraint.Constraint) -> tuple[float, formula.Formula]:
        '''
        TODO
        '''
        pass