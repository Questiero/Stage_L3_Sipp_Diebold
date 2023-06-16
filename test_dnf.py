from src.linearConstraint import LinearConstraint
from src.LPSolver import LPSolver
from src.revision import Revision
from src.integerVariable import IntegerVariable
from src.realVariable import RealVariable
from src.discreteL1DistanceFunction import discreteL1DistanceFunction
from src.daalmans import Daalmans

weights = {
    RealVariable.declare("x"): 1,
    RealVariable.declare("y"): 1,
}

solv = LPSolver()
simp = Daalmans(solv)

phi = LinearConstraint("x >= 0") & LinearConstraint("y <= 0") & LinearConstraint("x + y <= 4")
mu = (LinearConstraint("x + y >= 6") & LinearConstraint("x - 2*y >= -6") & LinearConstraint("x + 3*y >= 12") & LinearConstraint("x + 1/5*y <= 5"))\
    |(LinearConstraint("x + 1/5*y >= 5") & LinearConstraint("3*x + y >= 16") & LinearConstraint("x - y <= 4") & LinearConstraint("x <= 6") & LinearConstraint("x + y <= 9"))
rev = Revision(solv,  discreteL1DistanceFunction(weights,epsilon=1), simp, onlyOneSolution=False)
res = rev.execute(phi, mu)

print(str(res[0]) + "; " + str(res[1]))