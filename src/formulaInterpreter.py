import formula
import MLOSolver
import realVariable
import andOperator
import constraintOperator
from fractions import Fraction

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
            constraints = []
            for constraint in lc:
                constraintP = []
                for variable in variables:
                    if variable in constraint.variables:
                        constraintP.append(constraint.variables[variable])
                    else:
                        constraintP.append(0)
                constraints.append((constraintP, constraint.operator, constraint.bound))
            res = self.MLOSolver.solve(variables, list(map(lambda v : -1 if v == e else 0, variables)), constraints)
            if res[0] :
                if res[1][variables.index(e)] != 0:
                    return True
            
        return False

    def findAllSolutions(self, x) -> tuple[float, formula.Formula]:
        pass

    def findOneSolution(self, x) -> tuple[float, formula.Formula]:
        pass

    def optimizeCouple(self, phi : andOperator.And, mu : andOperator.And) -> tuple[float, formula.Formula]:
        '''
        TODO
        '''
        variables = list(andOperator.And(phi,mu).getVariables())
        e = realVariable.RealVariable("@")
        variables.append(e)

        constraints = []
        i = 0
        for formula in [phi, mu]:
            for lc in formula.getAdherence(e):
                for constraint in lc:
                    constraintP = []
                    for _ in range(0,(len(variables)) *i):
                        constraintP.append(0)
                    for variable in variables:
                        if variable in constraint.variables:
                            constraintP.append(constraint.variables[variable])
                        else:
                            constraintP.append(0)
                    for _ in range(0,(len(variables)) *(2-i)):
                        constraintP.append(0)
                    constraints.append((constraintP, constraint.operator, constraint.bound))
            i += 1

        for variable in variables:
            constraintP = []
            constraintN = []
            index = variables.index(variable)
            for i in range(0, len(variables)*3):
                if i == index:
                    constraintP.append(1)
                    constraintN.append(-1)
                elif i == index + len(variables):
                    constraintP.append(-1)
                    constraintN.append(1)
                elif i == index + len(variables)*2:
                    constraintP.append(-1)
                    constraintN.append(-1)
                else:
                    constraintP.append(0)
                    constraintN.append(0)
            constraints.append((constraintP, constraintOperator.ConstraintOperator.LEQ, 0))
            constraints.append((constraintN, constraintOperator.ConstraintOperator.LEQ, 0))

        obj = [0]*len(variables)*2
        for variable in variables: obj.append(Fraction(1,len(variables)-1))

        res = self.MLOSolver.solve(variables*3, obj, constraints)
        res = (res[0], res[1], Fraction(res[2]*(len(variables)-1)))

         