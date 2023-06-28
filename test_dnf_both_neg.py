from src.formula.nullaryFormula.constraint.linearConstraint import LinearConstraint
from src.mlo_solver.LPSolverRounded import LPSolverRounded
from src.revision import Revision
from src.variable.realVariable import RealVariable
from src.distance_function.discreteL1DistanceFunction import discreteL1DistanceFunction
from src.simplification.daalmans import Daalmans
from fractions import Fraction
from src.projector.floatConvexHullProjector import FloatConvexHullProjector

x = RealVariable.declare("x")
y = RealVariable.declare("y")

weights = {
    RealVariable.declare("x"): Fraction(1),
    RealVariable.declare("y"): Fraction(1),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplification=simplifier, rounding=12)

psi = ~LinearConstraint("x <= 0") & ~LinearConstraint("y <= 0") & ~LinearConstraint("x + y >= 4")
mu = (~LinearConstraint("x + y <= 6") & ~LinearConstraint("5*x + y >= 25") & ~LinearConstraint("-0.5*x + y >= 3") & ~LinearConstraint("1/3*x + y <= 4"))\
    | (~LinearConstraint("5*x + y <= 25") & ~LinearConstraint("3*x + y <= 16") & ~LinearConstraint("-x + y <= -4") & ~LinearConstraint("x >= 6") & ~LinearConstraint("x + y >= 9"))

rev = Revision(solver, discreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)

print("-------")
print(str(res[0]) + "; " + str(res[1]))

print("Satisfiable ?", simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()))

from src.formula.formulaDisplay import FormulaDisplay
display = FormulaDisplay()
display.display({psi.toLessOrEqConstraint() : 'blue', mu.toLessOrEqConstraint() : 'green', res[1].toLessOrEqConstraint() : 'red'}, [x,y])
