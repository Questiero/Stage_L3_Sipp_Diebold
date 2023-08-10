from src.formula import FormulaDisplay, LinearConstraint
from src.mlo_solver import LPSolverRounded
from src.revision import Revision
from src.variable import RealVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans
from src.projector import FloatConvexHullProjector

from fractions import Fraction

x = RealVariable.declare("x")
y = RealVariable.declare("y")

weights = {
    RealVariable.declare("x"): Fraction(1),
    RealVariable.declare("y"): Fraction(1),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplifiers=simplifier, rounding=10)

mu = LinearConstraint("x >= 2") & LinearConstraint("x <= 5") & LinearConstraint("y >= 2") & LinearConstraint("y <= 5")
psi = LinearConstraint("x >= 0") & LinearConstraint("x <= 7") & LinearConstraint("y >= 7") & LinearConstraint("y <= 9")\
| LinearConstraint("x >= 0") & LinearConstraint("x <= 7") & LinearConstraint("y >= -1") & LinearConstraint("y <= 0")\
| LinearConstraint("x >= 7") & LinearConstraint("x <= 9") & LinearConstraint("y >= 0") & LinearConstraint("y <= 7")\
| LinearConstraint("x >= -2") & LinearConstraint("x <= 0") & LinearConstraint("y >= 0") & LinearConstraint("y <= 7")

rev = Revision(solver, discreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)

print("-------")
print(str(res[0]) + "; " + str(res[1]))

print("Satisfiable ?", simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()))

from src.formula.formulaDisplay import FormulaDisplay
display = FormulaDisplay()
display.display({psi.toLessOrEqConstraint() : 'blue', mu.toLessOrEqConstraint() : 'green', res[1].toLessOrEqConstraint() : 'red'}, [x,y])
