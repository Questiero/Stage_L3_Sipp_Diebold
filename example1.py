from src.formula import LinearConstraint, PropositionalVariable
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
    
    PropositionalVariable("almondMilk"): Fraction("1e-6"),
    PropositionalVariable("banana"): Fraction(1),
    PropositionalVariable("bitter"): Fraction("1e6"),
    PropositionalVariable("cowMilk"): Fraction("1e-6"),
    PropositionalVariable("dessert"): Fraction("1e6"),
    PropositionalVariable("fruit"): Fraction("1e6"),
    PropositionalVariable("granulatedSugar"): Fraction("1e6"),
    PropositionalVariable("iceCube"): Fraction("1e6"),
    PropositionalVariable("kiwi"): Fraction(1),
    PropositionalVariable("milk"): Fraction("1e6"),
    PropositionalVariable("milkshake"): Fraction("1e6"),
    PropositionalVariable("soyMilk"): Fraction("1e-6"),
    PropositionalVariable("vanillaSugar"): Fraction("1e6"),

    RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("cowMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction("1e6"),
    RealVariable.declare("fruit_g", lowerBound = Fraction(0)): Fraction("1e6"),
    RealVariable.declare("granulatedSugar_g", lowerBound = Fraction(0)): Fraction("1e-6"),
    RealVariable.declare("iceCube_g", lowerBound = Fraction(0)): Fraction("1e6"),
    RealVariable.declare("kiwi_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("milk_g", lowerBound = Fraction(0)): Fraction("1e6"),
    RealVariable.declare("soyMilk_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction("1e6"),
    RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction("1e6"),

    IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(50),
    IntegerVariable.declare("granulatedSugar_tsp", lowerBound = Fraction(0)): Fraction(50),
    IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(50),
    IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(50),
    # Number of fruit types, a nonnegative integer (hence lowerBound to 0) with a heavy weight
    IntegerVariable.declare("nb_fruitTypes", lowerBound = Fraction(0)): Fraction("1e6"),
    IntegerVariable.declare("vanillaSugar_u", lowerBound = Fraction(0)): Fraction(50),

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
dk =  PropositionalVariable("banana") >> PropositionalVariable("fruit")\
     & (PropositionalVariable("kiwi") >> PropositionalVariable("fruit"))

# Règle...
dk &=  LinearConstraint("fruit_g - banana_g - kiwi_g = 0")\
     & LinearConstraint("food_g - fruit_g - milk_g - granulatedSugar_g - iceCube_g - vanillaSugar_g = 0")\
     & LinearConstraint("milk_g - almondMilk_g - cowMilk_g - soyMilk_g = 0")

# Règle...
dk &=  LinearConstraint("banana_g - 115 * banana_u = 0")\
     & LinearConstraint("cowMilk_g - 1030 * cowMilk_L = 0")\
     & LinearConstraint("soyMilk_g - 1030 * soyMilk_L = 0")\
     & LinearConstraint("almondMilk_g - 1030 * almondMilk_L = 0")\
     & LinearConstraint("kiwi_g -  100 * kiwi_u = 0")\
     & LinearConstraint("vanillaSugar_g - 7.5 * vanillaSugar_u = 0")\
     & LinearConstraint("granulatedSugar_g - 15 * granulatedSugar_tsp = 0")\
     & LinearConstraint("iceCube_g - 24.759 * iceCube_u = 0")

# Règle...
dk &= LinearConstraint("sweeteningPower_g  - granulatedSugar_g\
                                           - 0.158 * banana_g\
                                           - 0.0899 * kiwi_g\
                                           - 0.98 * vanillaSugar_g\
                                           - 0.0489 * cowMilk_g\
                                           - 0.0368 * soyMilk_g\
                                           - 0.04 * almondMilk_g = 0")

# Règle...
dk &=   ((PropositionalVariable("almondMilk") | PropositionalVariable("cowMilk") | PropositionalVariable("soyMilk"))\
     // PropositionalVariable("milk"))

# Règle...
dk &=   ((PropositionalVariable("cowMilk") | PropositionalVariable("soyMilk")) & PropositionalVariable("kiwi")) \
     >> PropositionalVariable("bitter")

# Règle...
dk &=  (PropositionalVariable("milkshake") >> PropositionalVariable("dessert"))\
     & (PropositionalVariable("dessert") >> ~PropositionalVariable("bitter"))

# Règle...
dk &=  (PropositionalVariable("banana") // ~LinearConstraint(f"banana_g <= 0"))\
     & (PropositionalVariable("kiwi") // ~LinearConstraint(f"kiwi_g <= 0"))\
     & (PropositionalVariable("cowMilk") // ~LinearConstraint(f"cowMilk_g <= 0"))\
     & (PropositionalVariable("soyMilk") // ~LinearConstraint(f"soyMilk_g <= 0"))\
     & (PropositionalVariable("almondMilk") // ~LinearConstraint(f"almondMilk_g <= 0"))\
     & (PropositionalVariable("granulatedSugar") // ~LinearConstraint("granulatedSugar_g <= 0"))\
     & (PropositionalVariable("vanillaSugar") // ~LinearConstraint("vanillaSugar_g <= 0"))\
     & (PropositionalVariable("iceCube") // ~LinearConstraint("iceCube_g <= 0"))\

# Règle...
dk &= LinearConstraint("nb_fruitTypes - b2i_banana - b2i_kiwi = 0")

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case... (variables dans le même ordre que article)
x_src =  LinearConstraint("banana_u = 2")\
     & LinearConstraint("vanillaSugar_u = 2")\
     & LinearConstraint("cowMilk_g = 1030.")\
     & LinearConstraint("granulatedSugar_tsp = 4")\
     & LinearConstraint("iceCube_u = 4")\
     & LinearConstraint("kiwi_g = 0")\
     & LinearConstraint("soyMilk_g = 0.")\
     & LinearConstraint("almondMilk_g = 0.")\
     & PropositionalVariable("milkshake")\

# Target problem...
y_trgt = PropositionalVariable("kiwi") & PropositionalVariable("milkshake")

res = adaptator.execute(x_src, y_trgt, dk)