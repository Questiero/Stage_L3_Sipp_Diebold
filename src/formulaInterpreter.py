from .formula import Formula
from .MLOSolver import MLOSolver
from .realVariable import RealVariable
from .andOperator import And
from .constraintOperator import ConstraintOperator
from fractions import Fraction
from .linearConstraint import LinearConstraint
from .variable import Variable
from .distanceFunction import DistanceFunction
from .notOperator import Not
from .simplification import Simplification
from .orOperator import Or

class FormulaInterpreter:
    def __init__(self, mloSolver : MLOSolver, distanceFunction : DistanceFunction, simplification : Simplification, onlyOneSolution : bool) -> None:
        self.__MLOSolver = mloSolver
        self.__distanceFunction = distanceFunction
        self.__onlyOneSolution = onlyOneSolution
        self.__simplifier = simplification
        if(self.__simplifier != None):
            self.__simplifier._interpreter = self
        self._eVar = RealVariable("@")

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
        if self.__simplifier == None:
            return phi
        else:
            orChild = []
            for miniPhi in phi.children:
                orChild.append(self.__simplifier.run(miniPhi))
            return Or(formulaSet= set(orChild))

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
        variables.append(self._eVar)

        for lc in phi.getAdherence(self._eVar):
            constraints = []
            for constraint in lc:
                constraintP = []
                for variable in variables:
                    if variable in constraint.variables:
                        constraintP.append(constraint.variables[variable])
                    else:
                        constraintP.append(0)
                constraints.append((constraintP, constraint.operator, constraint.bound))
            constraintP = []
            for var in variables: 
                if(var == self._eVar) :
                    constraintP.append(-1)
                else :
                    constraintP.append(0)
            constraints.append((constraintP, ConstraintOperator.LEQ, 0))
                    
            res = self.__MLOSolver.solve(variables, list(map(lambda v : -1 if v == self._eVar else 0, variables)), constraints)
            if res[0] :
                if res[1][variables.index(self._eVar)] != 0:
                    return True
            
        return False

    def findAllSolutions(self, variables : dict[Variable], phi : And, mu : And) -> tuple[Fraction, Formula]:
        '''
         Method used for find all solutions for the optimization of a couple of Formula

        Attributes
        ----------
        variables : list of variables
        phi : a formula (And)
        mu : a formula (And)

        Returns
        -------
        res: distance between phi and mu, Formula wich symbolize the optimisation between phi and mu
        '''
        pass

    def findOneSolution(self, variables : list[Variable], phi : And, mu : And) -> tuple[Fraction, Formula]:
        '''
        Method used for find one solution for the optimization of a couple of Formula

        Attributes
        ----------
        variables : list of variables
        phi : a formula (And)
        mu : a formula (And)

        Returns
        -------
        res: distance between phi and mu, Formula wich symbolize the optimisation between phi and mu
        
        '''
        constraints = self.__buildConstraints(variables, phi, mu)

        obj = [0]*len(variables)*2
        for variable in variables:
            obj.append(self.__distanceFunction.getWeights()[variable])
        res = self.__MLOSolver.solve(variables*3, obj, constraints)
        if(not res[0]): 
            raise Exception("Optimize couple impossible") 
        
        values = res[1]
        resSet = set([])
        for i in range(0,len(variables)):
            if variables[i].name != "@":
                resSet = resSet.union(set([LinearConstraint(str(variables[i]) + " = " + str(Fraction(values[len(variables)+i])))]))
        return (res[2], And(formulaSet=resSet))

    def __buildConstraints(self, variables : list[Variable], phi : And, mu : And) -> dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]:
        '''
        Method used to build table of constraints, for the solver, linked to phi and mu
        Attributes
        ----------
        variables : list of variables
        phi : a formula (And)
        mu : a formula (And)

        Returns
        -------
        res: table of constraint wich simbolyze all of constraints of phi and mu
        '''
        constraints = []
        i = 0
        for formula in [phi, mu]:
            for lc in formula.getAdherence(self._eVar):
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
        return constraints

    def optimizeCouple(self, phi : And, mu : And) -> tuple[Fraction, Formula]:
        '''
        Method used for optimized a couple of Formula

        Attributes
        ----------
        phi : a formula (And)
        mu : a formula (And)

        Returns
        -------
        res: distance between phi and mu, Formula wich symbolize the optimisation between phi and mu
        '''
        variables = list(And(phi,mu).getVariables())
        e = RealVariable("@")
        variables.append(e)
        self.__distanceFunction.getWeights()[e] = 0

        if self.__onlyOneSolution:
            return self.findOneSolution(variables,phi,mu)
        else:
            return self.findAllSolutions(variables,phi,mu)
    

    def removeNot(self, phi: And):
        andSet = set()
        for andChild in phi.children:
            if isinstance(andChild, Not):
                andSet.add(andChild.copyNegLitteral(self._eVar))
            else:
                andSet.add(andChild)
            
        return And(formulaSet = andSet)
         