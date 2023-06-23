from src.linearConstraint import LinearConstraint
from src.LPSolverRounded import LPSolverRounded
from src.revision import Revision
from src.realVariable import RealVariable
from src.discreteL1DistanceFunction import discreteL1DistanceFunction
from src.caron import Caron
from src.daalmans import Daalmans
from fractions import Fraction

weights = {
    RealVariable.declare("vol_tequila"): Fraction(1),
    RealVariable.declare("vol_sirop"): Fraction(1),
    RealVariable.declare("vol_alcool"): Fraction(20),
    RealVariable.declare("pouvoirSucrant"): Fraction(20),
}

solver = LPSolverRounded()
simplifier = [Caron(solver), Daalmans(solver)]

cd = LinearConstraint("vol_tequila >= 0") & LinearConstraint("0.35*vol_tequila - vol_alcool = 0")\
    & LinearConstraint("0.6*vol_sirop + 0.2 * vol_tequila - pouvoirSucrant = 0")
psi = LinearConstraint("vol_tequila = 4") & LinearConstraint("vol_sirop = 2") & cd
mu = LinearConstraint("vol_alcool = 0") & cd

rev = Revision(solver, discreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False)
res = rev.execute(psi, mu)

print("-------")
print(str(res[0]) + "; " + str(res[1]))