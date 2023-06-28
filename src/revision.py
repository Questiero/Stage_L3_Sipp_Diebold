from .formula import Formula
from .mlo_solver.MLOSolver import MLOSolver
from .distance_function.distanceFunction import DistanceFunction
from .formulaInterpreter import FormulaInterpreter
from .formula.naryFormula.orOperator import Or
from .formula.naryFormula.andOperator import And
from .formula.unaryFormula.unaryFormula import UnaryFormula
from .formula.nullaryFormula.nullaryFormula import NullaryFormula
from .formula.nullaryFormula.constraint.linearConstraint import LinearConstraint
from .formula.unaryFormula.notOperator import Not
from .constants import Constants
from fractions import Fraction
from .formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from .simplification.simplification import Simplification
from .projector import Projector
import math

class Revision:
    
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    __projector : Projector
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplification] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, projector: Projector = None):
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, simplifiers)
        self._onlyOneSolution = onlyOneSolution

        self.__projector = projector

    def execute(self, psi : Formula, mu : Formula) -> tuple[Fraction, Formula]:
        psiDNF, muDNF = psi.toLessOrEqConstraint().toDNF(), mu.toLessOrEqConstraint().toDNF()
        return self.__executeDNF(self.__convertExplicit(psiDNF), self.__convertExplicit(muDNF))
        
    def __executeDNF(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        
        res = None
        disRes = None

        if(self._onlyOneSolution):
            
            for minipsi in psi.children:
                for miniMu in mu.children:
                    
                    lit = self.__executeLiteral(minipsi, miniMu)

                    if not (lit[0] is None):
                        if (disRes is None):
                            disRes = lit[0]
                            res = lit[1]
                        elif (disRes > lit[0]):
                            disRes = lit[0]
                            res = lit[1]
                    else:
                        if (disRes is None) & (res is None):
                            res = lit[1]

        else:

            setRes = set()
            
            for minipsi in psi.children:
                for miniMu in mu.children:
                    
                    lit = self.__executeLiteral(minipsi, miniMu)
                    print("---")
                    print(str(lit[0]) + "; " + str(lit[1]))
                    
                    if not (lit[0] is None):
                        if (disRes is None):
                            disRes = lit[0]
                            setRes = {lit[1]}
                        elif (disRes == lit[0]):
                            setRes.add(lit[1])
                        elif (disRes > lit[0]):
                            disRes = lit[0]
                            setRes = {lit[1]}
                    else:
                        if (disRes is None):
                            setRes.add(lit[1])
            
            res = Or(formulaSet = setRes).toDNF()

        return (disRes, self.__interpreter.simplifyMLC(res.toLessOrEqConstraint().toDNF()))
    
    def __executeLiteral(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:

        # first step: check if psi and mu are coherent
        if((not self.__interpreter.sat(psi)) or (not self.__interpreter.sat(mu))):
            return (None, mu) # None = inf
        
        # second step: find dStar (and psiPrime if onlyOneSoltuion)
        dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(psi), self.__interpreter.removeNot(mu))

        # third step: lambdaEpsilon
        epsilon = self.__distance._epsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # fourth step: find psiPrime (only if not onlyOneSolution)
        if(not self._onlyOneSolution):
            psiPrime = self.__expand(psi, lambdaEpsilon)
    
        # fifth step
        if dStar % epsilon != 0:
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            lambdaEpsilon = dStar + epsilon
            psiPrime = self.__expand(psi, lambdaEpsilon)
            return(dStar, psiPrime & mu)
    
    def __executeConstraint(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        return self.__interpreter.optimizeCouple(psi, mu)
    
    def __convertExplicit(self, phi: Formula) -> Formula:
        
        if isinstance(phi, And):
            return Or(phi)
        elif isinstance(phi, UnaryFormula) | isinstance(phi, NullaryFormula):
            return Or(And(phi))
        else:
            orSet = set()
            for miniPhi in phi.children:
                if isinstance(miniPhi, And):
                    orSet.add(miniPhi)
                else:
                    orSet.add(And(miniPhi))
            return Or(formulaSet = orSet)

    def __expand(self, psi: Formula, lambdaEpsilon: Fraction) -> Formula:
        
        yVariables = {v: v.__class__.declareAnonymous(ending = ("y" + str(v.name))) for v in psi.getVariables()}

        constraints = list()

        # Create x in M(psi) constraints and change variables
        for minipsi in psi.children:
            if isinstance(minipsi, Not):
                const = minipsi.children.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(Not(const))
            else:
                const = minipsi.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(const)

        # Add distance function constraints
        zVariables = {v: v.__class__.declareAnonymous(ending = ("z" + str(v.name))) for v in psi.getVariables()}
        for yVar in yVariables:
            z = zVariables[yVar]
            # Creating link between x, y and z
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(-1)
            const.variables[yVariables[yVar]] = Fraction(1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(1)
            const.variables[yVariables[yVar]] = Fraction(-1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            # Keeping z in memory
            zVariables[yVar] = z

        # TODO pas sûr de mon code, à tester
        # TODO fonction de distance, les poids ?
        # Generate distance constraint
        distanceConstraint = LinearConstraint("")
        distanceConstraint.operator = ConstraintOperator.LEQ
        distanceConstraint.bound = lambdaEpsilon
        for z in zVariables:
            distanceConstraint.variables[zVariables[z]] = self.__distance.getWeights()[z]
        constraints.append(distanceConstraint)

        return self.__projector.projectOn(And(formulaSet = set(constraints)), yVariables.keys())

        #try:
        #    return self.__projector.projectOn(And(formulaSet = set(constraints)), yVariables.keys())
        #except RuntimeError:
        #    if isinstance(psi, NaryFormula):
        #        return And(formulaSet = {self.__expandLiteral(c, lambdaEpsilon) for c in psi.children})
        #    else:
        #        return self.__expandLiteral(psi, lambdaEpsilon)

    def __expandLiteral(self, psi: Formula, lambdaEpsilon: Fraction):
        
        if isinstance(psi, Not):

            lc = psi.children.clone()
            
            match lc.operator:
                case ConstraintOperator.LEQ:
                    lc.bound += lambdaEpsilon
                case ConstraintOperator.GEQ:
                    lc.bound -= lambdaEpsilon
                case ConstraintOperator.EQ:
                    return And(formulaSet = {Not(self.__expandLiteral(c)) for c in psi.toLessOrEqConstraint().children})

            return Not(lc)

        else:

            lc = psi.clone()

            match lc.operator:
                case ConstraintOperator.LEQ:
                    lc.bound += lambdaEpsilon
                case ConstraintOperator.GEQ:
                    lc.bound -= lambdaEpsilon
                case ConstraintOperator.EQ:
                    return And(formulaSet = {self.__expandLiteral(c) for c in psi.toLessOrEqConstraint().children})

            return lc