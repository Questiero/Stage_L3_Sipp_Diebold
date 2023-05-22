from formula import Formula
from MLOSolver import MLOSolver
from realVariable import RealVariable
from andOperator import And
from constraintOperator import ConstraintOperator
from fractions import Fraction
from linearConstraint import LinearConstraint
from variable import Variable

class FormulaInterpreter:
    def __init__(self, mloSolver : MLOSolver) -> None:
        self.MLOSolver = mloSolver

    def simplifyMLC(self, phi : Formula):
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

    def sat(self, phi : Formula) -> bool:
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
        e = RealVariable("@")
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
            res = self.solve(variables, list(map(lambda v : -1 if v == e else 0, variables)), constraints)
            if res[0] :
                if res[1][variables.index(e)] != 0:
                    return True
            
        return False

    def findAllSolutions(self, x) -> tuple[float, Formula]:
        '''
        
        '''
        pass

    def findOneSolution(self, variables : dict[Variable], values : dict[float]) -> tuple[float, Formula]:
        '''
        
        
        '''
        resSet = set([])
        for i in range(0,len(variables)):
            if variables[i].name != "@":
                resSet = resSet.union(set([LinearConstraint(str(variables[i]) + " = " + str(Fraction(values[len(variables)+i])))]))
        return And(formulaSet=resSet)

    def optimizeCouple(self, phi : And, mu : And) -> tuple[float, Formula]:
        '''
        TODO
        '''
        variables = list(And(phi,mu).getVariables())
        e = RealVariable("@")
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
            constraints.append((constraintP, ConstraintOperator.LEQ, 0))
            constraints.append((constraintN, ConstraintOperator.LEQ, 0))

        obj = [0]*len(variables)*2
        for variable in variables: obj.append(Fraction(1,1))

        res = self.MLOSolver.solve(variables*3, obj, constraints)
        return (self.findOneSolution(variables, res[1]), Fraction(res[2]))
         