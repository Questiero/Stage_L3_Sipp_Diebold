from src.formula import LinearConstraint, PropositionalVariable
from src.mlo_solver import  ScipySolverRounded
from src import Adaptation
from src.variable import RealVariable, IntegerVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    
    # Presence of almond milk, a boolean variable with a light weight
    PropositionalVariable("almondMilk"): Fraction("1e-6"),
    # Presence of banana, a boolean variable with a TODO
    PropositionalVariable("banana"): Fraction(1),
    # Presence of bitterness, a boolean variable with a heavy weight
    PropositionalVariable("bitter"): Fraction("1e6"),
    # Presence of cow milk, a boolean variable with a light weight
    PropositionalVariable("cowMilk"): Fraction("1e-6"),
    # Is the recipe for a dessert, a boolean variable with a heavy weight
    PropositionalVariable("dessert"): Fraction("1e6"),
    # Presence of fruit, a boolean variable with a heavy weight
    PropositionalVariable("fruit"): Fraction("1e6"),
    # Presence of granulated sugar, a boolean variable with a heavy weight
    PropositionalVariable("granulatedSugar"): Fraction("1e6"),
    # Presence of ice cubes, a boolean variable with a heavy weight
    PropositionalVariable("iceCube"): Fraction("1e6"),
    # Presence of kiwi, a boolean variable with a TODO
    PropositionalVariable("kiwi"): Fraction(1),
    # Presence of milk, a boolean variable with a heavy weight
    PropositionalVariable("milk"): Fraction("1e6"),
    # Is the recipe for a milkshake, a boolean variable with a heavy weight
    PropositionalVariable("milkshake"): Fraction("1e6"),
    # Presence of soy milk, a boolean variable with a light weight
    PropositionalVariable("soyMilk"): Fraction("1e-6"),
    # Presence of vanilla sugar, a boolean variable with a heavy weight
    PropositionalVariable("vanillaSugar"): Fraction("1e6"),

    # Mass (in grams) of almond milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of almond milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass (in grams) of banana, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of cow milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of cow milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("cowMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass (in grams) of food, a nonnegative real (hence lowerBound to 0) with a heavy weight
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction("1e6"),
    # Mass (in grams) of fruit, a nonnegative real (hence lowerBound to 0) with a heavy weight
    RealVariable.declare("fruit_g", lowerBound = Fraction(0)): Fraction("1e6"),
    # Mass (in grams) of granulated sugar, a nonnegative real (hence lowerBound to 0) with a light weight
    RealVariable.declare("granulatedSugar_g", lowerBound = Fraction(0)): Fraction("1e-6"),
    # Mass (in grams) of ice cube, a nonnegative real (hence lowerBound to 0) with a heavy weight
    RealVariable.declare("iceCube_g", lowerBound = Fraction(0)): Fraction("1e6"),
    # Mass (in grams) of kiwi, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("kiwi_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of milk, a nonnegative real (hence lowerBound to 0) with a heavy weight
    RealVariable.declare("milk_g", lowerBound = Fraction(0)): Fraction("1e6"),
    # Mass (in grams) of soy milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("soyMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of soy milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Sweetening power (in grams) of the recipe in grams, a nonnegative real (hence lowerBound to 0) with a heavy weight
    RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction("1e6"),
    # Mass (in grams) of vanilla sugar, a nonnegative real (hence lowerBound to 0) with an heavy weight
    RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction("1e6"),

    # Number of bananas, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(50),
    # Number of teaspoons of granulated sugar, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("granulatedSugar_tsp", lowerBound = Fraction(0)): Fraction(50),
    # Number of ice cubes, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(50),
    # Number of kiwis, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(50),
    # Number of fruit types, a nonnegative integer (hence lowerBound to 0) with a heavy weight
    IntegerVariable.declare("nb_fruitTypes", lowerBound = Fraction(0)): Fraction("1e6"),
    # Number of bags of vanilla sugar, a nonnegative integer (hence lowerBound to 0) with a TODO
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
dk &=  (PropositionalVariable("banana") // ~LinearConstraint("banana_g <= 0"))\
     & (PropositionalVariable("kiwi") // ~LinearConstraint("kiwi_g <= 0"))\
     & (PropositionalVariable("cowMilk") // ~LinearConstraint("cowMilk_g <= 0"))\
     & (PropositionalVariable("soyMilk") // ~LinearConstraint("soyMilk_g <= 0"))\
     & (PropositionalVariable("almondMilk") // ~LinearConstraint("almondMilk_g <= 0"))\
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