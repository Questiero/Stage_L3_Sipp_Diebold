from src.linearConstraint import LinearConstraint
from src.LPSolver import LPSolver
from src.revision import Revision
from src.integerVariable import IntegerVariable
from src.realVariable import RealVariable
from src.discreteL1DistanceFunction import discreteL1DistanceFunction
from src.daalmans import Daalmans

weights = {
    IntegerVariable.declare("quant_rondelleCitron"): 1,
    RealVariable.declare("vol_tequila"): 1,
    RealVariable.declare("vol_sirop"): 1,
    RealVariable.declare("vol_jusCitronVert"): 1,
    RealVariable.declare("vol_vodka"): 1,
    RealVariable.declare("vol_alcool"): 20,
    RealVariable.declare("pouvoirSucrant"): 20,
}

solv = LPSolver()
simp = Daalmans(solv)

cd = LinearConstraint("vol_tequila >= 0") & LinearConstraint("vol_vodka >= 0")\
    & LinearConstraint("0.35*vol_tequila + 0.45*vol_vodka  - vol_alcool = 0")\
    & LinearConstraint("0.6*vol_sirop + 0.2 * vol_tequila + 0.2 * vol_vodka - pouvoirSucrant = 0")
phi = LinearConstraint("vol_tequila = 4") & LinearConstraint("vol_sirop = 2")\
    & LinearConstraint("quant_rondelleCitron = 1") & LinearConstraint("vol_jusCitronVert >= 2")\
    & LinearConstraint("vol_jusCitronVert <= 3") & cd
mu = LinearConstraint("vol_alcool = 0") & cd

rev = Revision(solv, discreteL1DistanceFunction(weights), simp, onlyOneSolution=True)
res = rev.execute(phi, mu)

print(str(res[0]) + "; " + str(res[1]))