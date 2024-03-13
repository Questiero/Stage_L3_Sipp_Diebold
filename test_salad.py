from src.formula import LinearConstraint, PropositionalVariable, EnumeratedType
from src.mlo_solver import  ScipySolverRounded
from src import Adaptation
from src.variable import RealVariable, IntegerVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans
from src.projector import FloatConvexHullProjector

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    PropositionalVariable("lettuce"): Fraction(1),
    PropositionalVariable("escarole"): Fraction(1),
    PropositionalVariable("greenSalad"): Fraction(1),
    PropositionalVariable("bacon"): Fraction(1),
    PropositionalVariable("vinegar"): Fraction(1),
    PropositionalVariable("saladDish"): Fraction(1),
    PropositionalVariable("oliveOil"): Fraction(1),
    PropositionalVariable("lemonJuice"): Fraction(1),
    PropositionalVariable("water"): Fraction(1),

    RealVariable.declare("lettuce_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("escarole_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("greenSalad_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("bacon_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("vinegar_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("oliveOil_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("lemonJuice_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("water_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("water_L", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("vinegar_L", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("oliveOil_L", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("lemonJuice_L", lowerBound = Fraction(0)): Fraction(1),

    IntegerVariable.declare("lettuce_u", lowerBound = Fraction(0)): Fraction(1),
    IntegerVariable.declare("escarole_u", lowerBound = Fraction(0)): Fraction(1),
    IntegerVariable.declare("bacon_u", lowerBound = Fraction(0)): Fraction(1),

    RealVariable.declare("ak1"): Fraction(1),
    RealVariable.declare("ak2"): Fraction(1)
}

"""
     INITATIALIZATION OF THE SOLVER
"""

solver = ScipySolverRounded()
simplifier = [Daalmans(solver)]
adaptator = Adaptation(solver, discreteL1DistanceFunction(weights, epsilon=Fraction("1e-4")), simplifier, onlyOneSolution=True)

adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# Règle...
dk =  ((PropositionalVariable("escarole") | PropositionalVariable("lettuce")) // PropositionalVariable("greenSalad"))\
    & (PropositionalVariable("saladDish") >> PropositionalVariable("greenSalad"))

# Règle...
dk &= LinearConstraint("greenSalad_g - lettuce_g - escarole_g = 0")\
    & LinearConstraint("food_g - greenSalad_g - bacon_g - vinegar_g - oliveOil_g - lemonJuice_g - water_g = 0")

# Règle...
dk &= LinearConstraint("water_g - 1000 * water_L = 0")\
    & LinearConstraint("escarole_g - 530 * escarole_u = 0")\
    & LinearConstraint("lettuce_g - 344 * lettuce_u = 0")\
    & LinearConstraint("bacon_g - 15 * bacon_u = 0")\
    & LinearConstraint("vinegar_g - 1010 * vinegar_L = 0")\
    & LinearConstraint("oliveOil_g - 913.7 * oliveOil_L = 0")\
    & LinearConstraint("lemonJuice_g - 1100 * lemonJuice_L = 0")

# Règle...
dk &= (PropositionalVariable("water") // ~LinearConstraint("water_g <= 0"))\
    & (PropositionalVariable("escarole") // ~LinearConstraint("escarole_g <= 0"))\
    & (PropositionalVariable("lettuce") // ~LinearConstraint("lettuce_g <= 0"))\
    & (PropositionalVariable("bacon") // ~LinearConstraint("bacon_g <= 0"))\
    & (PropositionalVariable("vinegar") // ~LinearConstraint("vinegar_g <= 0"))\
    & (PropositionalVariable("oliveOil") // ~LinearConstraint("oliveOil_g <= 0"))\
    & (PropositionalVariable("lemonJuice") // ~LinearConstraint("lemonJuice_g <= 0"))

# Adaptation Knowledge...
ak = LinearConstraint("ak1 - vinegar_g + water_g + lemonJuice_g = 0")\
    & LinearConstraint("ak2 - water_g + lemonJuice_g = 0")

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case... (variables dans le même ordre que article)
x_src = PropositionalVariable("saladDish")\
    & LinearConstraint("lettuce_u = 2")\
    & LinearConstraint("vinegar_g = 40")\
    & LinearConstraint("oliveOil_g = 50")\
    & LinearConstraint("bacon_u = 6")

# Target problem...
y_trgt = PropositionalVariable("saladDish")\
    & ~PropositionalVariable("vinegar")\
    & ~PropositionalVariable("lettuce")

res = adaptator.execute(x_src, y_trgt, dk & ak)