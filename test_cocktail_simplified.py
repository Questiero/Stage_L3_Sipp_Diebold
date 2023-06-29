from src.formula import LinearConstraint
from src.mlo_solver import LPSolverRounded
from src.revision import Revision
from src.variable import RealVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans
from src.projector import FloatConvexHullProjector

from fractions import Fraction

weights = {
    RealVariable.declare("vol_tequila"): Fraction(1),
    RealVariable.declare("vol_sirop"): Fraction(1),
    RealVariable.declare("vol_alcool"): Fraction(20),
    RealVariable.declare("pouvoirSucrant"): Fraction(20),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplification=simplifier, rounding=10)

cd = LinearConstraint("vol_tequila >= 0") & LinearConstraint("0.35*vol_tequila - vol_alcool = 0")\
    & LinearConstraint("0.6*vol_sirop + 0.2 * vol_tequila - pouvoirSucrant = 0")
psi = LinearConstraint("vol_tequila = 4") & LinearConstraint("vol_sirop = 2") & cd
mu = LinearConstraint("vol_alcool = 0") & cd

rev = Revision(solver, discreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)

print("-------")
print(str(res[0]) + "; " + str(res[1]))

print("Satisfiable ?", simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()))