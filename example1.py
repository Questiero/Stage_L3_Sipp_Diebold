from src.formula import LinearConstraint, PropositionalVariable, FormulaManager
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
    
    # Presence of almond milk, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("almondMilk", fmName="almondMilk"): Fraction(1),
    # Presence of banana, a boolean variable with a TODO
    PropositionalVariable("banana", fmName="banana"): Fraction(1),
    # Presence of bitterness, a boolean variable with a weight associated to a property of a recipe
    PropositionalVariable("bitter", fmName="bitter"): Fraction(100),
    # Presence of cow milk, a boolean variable with a light weight TODO
    PropositionalVariable("cowMilk", fmName="cowMilk"): Fraction(1),
    # Is the recipe for a dessert, a boolean variable with a weight associated to a property of a recipe
    PropositionalVariable("dessert", fmName="dessert"): Fraction(100),
    # Presence of fruit, a boolean variable with a weight associated to category of ingredients
    PropositionalVariable("fruit", fmName="fruit"): Fraction(10),
    # Presence of kiwi, a boolean variable with a TODO
    PropositionalVariable("kiwi", fmName="kiwi"): Fraction(1),
    # Presence of milk, a boolean variable with a heavy weight TODO
    PropositionalVariable("milk", fmName="milk"): Fraction(10),
    # Is the recipe for a milkshake, a boolean variable with a weight associated to a complete recipe
    PropositionalVariable("milkshake", fmName="milkshake"): Fraction(1000),
    # Presence of soy milk, a boolean variable with a light weight TODO
    PropositionalVariable("soyMilk", fmName="soyMilk"): Fraction(1),

    # Mass (in grams) of almond milk, a nonnegative real (hence lowerBound to 0) with a weight of 1, chosen as the weight of a gram of food
    RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of almond milk, a nonnegative real (hence lowerBound to 0) with a a weight equal to the volumic mass of one liter of milk (1030g/L) multiplied by the weight of a gram of milk
    RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass (in grams) of banana, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of cow milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of cow milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("cowMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass (in grams) of food, a nonnegative real (hence lowerBound to 0) with a weight associated to a wide category of ingredients/property of the recipe
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(100),
    # Mass (in grams) of fruit, a nonnegative real (hence lowerBound to 0) with a weight associated to a category of ingredients
    RealVariable.declare("fruit_g", lowerBound = Fraction(0)): Fraction(10),
    # Mass (in grams) of granulated sugar, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("granulatedSugar_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of ice cube, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("iceCube_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of kiwi, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("kiwi_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass (in grams) of milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("milk_g", lowerBound = Fraction(0)): Fraction(10),
    # Mass (in grams) of soy milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("soyMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of soy milk, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Sweetening power (in grams) of the recipe in grams, a nonnegative real (hence lowerBound to 0) with a weight associated to a property of the recipe
    RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction(100),
    # Mass (in grams) of vanilla sugar, a nonnegative real (hence lowerBound to 0) with a TODO
    RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction(1),

    # Number of bananas, a nonnegative integer (hence lowerBound to 0) with a with a weight equal to the average mass of a banana (115g/u) multiplied by the weight of a gram of banana
    IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(115),
    # Number of teaspoons of granulated sugar, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("granulatedSugar_tbsp", lowerBound = Fraction(0)): Fraction(15),
    # Number of ice cubes, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(24.759),
    # Number of kiwis, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(100),
    # Number of fruit types, a nonnegative integer (hence lowerBound to 0) with a weight associated to a property of the recipe that preserves the number of fruit types
    IntegerVariable.declare("nb_fruitTypes", lowerBound = Fraction(0)): Fraction(100),
    # Number of bags of vanilla sugar, a nonnegative integer (hence lowerBound to 0) with a TODO
    IntegerVariable.declare("vanillaSugar_u", lowerBound = Fraction(0)): Fraction(7.5),

}

"""
     INITATIALIZATION OF THE SOLVER
"""

# Declaration of the MLO Solver used for this example.
# Here, we chose to use a rounded (to limit floating points erros) version of HiGHS using Scipy's wrapper.
solver = ScipySolverRounded()

# Declaration of the simplification algorithms used for this example.
# Here, we chose to only use Daalmans' algorithm.
simplifiers = [Daalmans(solver)]

# Declaration of the discretized Manhattan distance function used for this example, using the weights declared above and an epsilon of 1e-4.
distanceFunction = discreteL1DistanceFunction(weights, epsilon=Fraction("1e-4"))

# Declaration of the Adaptation object used for this example, using all the variables declared beforehand and specifying
# that we wish to have only one valid solution instead of all the possible ones.
adaptator = Adaptation(solver, distanceFunction, simplifiers, onlyOneSolution=True)

# Preloading the adaptator, initializaing all the b2i_ variables and making it so the user can use them in the following parts of the script
# (Necessary for DK8, the nb_fruitTypes constraint)
adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# DK1: Bananas and kiwis are fruits.
dk = FormulaManager.parser("(banana -> fruit) & (kiwi -> fruit)")

# DK2: For each food type and unit, there is a known correspondence of one unit of this food type to its mass,
#      e.g. the mass of 1 banana and the mass of 1 tablespoon of granulated sugar.
# Source: Mass coming from USDA (https://fdc.nal.usda.gov/)
#                          Vahine (URL) (for vanilla sugar)
dk &=  LinearConstraint("banana_g - 115 * banana_u = 0")\
     & LinearConstraint("cowMilk_g - 1030 * cowMilk_L = 0")\
     & LinearConstraint("soyMilk_g - 1030 * soyMilk_L = 0")\
     & LinearConstraint("almondMilk_g - 1030 * almondMilk_L = 0")\
     & LinearConstraint("kiwi_g - 100 * kiwi_u = 0")\
     & LinearConstraint("vanillaSugar_g - 7.5 * vanillaSugar_u = 0")\
     & LinearConstraint("granulatedSugar_g - 15 * granulatedSugar_tbsp = 0")\
     & LinearConstraint("iceCube_g - 24.759 * iceCube_u = 0")

# DK3: Relation between each type of food and its subtypes in the taxonomy (TODO reprendre après envoie)
# Source: The sweetening power of each ingredient is coming from USDA (https://fdc.nal.usda.gov/)
# The sweetening power is known for every ingredient type, e.g. 0.158 for bananas (1 gram of banana has the same sweetening power as 0.158 gram of granulated sugar), 1 for granulated sugar, etc.
dk &= LinearConstraint("sweeteningPower_g  - granulatedSugar_g\
                                           - 0.158 * banana_g\
                                           - 0.0899 * kiwi_g\
                                           - 0.98 * vanillaSugar_g\
                                           - 0.0489 * cowMilk_g\
                                           - 0.0368 * soyMilk_g\
                                           - 0.04 * almondMilk_g = 0")\
     & LinearConstraint("fruit_g - banana_g - kiwi_g = 0")\
     & LinearConstraint("food_g - fruit_g - milk_g - granulatedSugar_g - iceCube_g - vanillaSugar_g = 0")\
     & LinearConstraint("milk_g - almondMilk_g - cowMilk_g - soyMilk_g = 0")

# DK4: Almond milk, cow milk and soy milk are 3 types of milks (and, to make it simpler, it can be assumed that there
#      are no other types of milk in my fridge).
dk &= FormulaManager.parser("(almondMilk | cowMilk | soyMilk) <-> milk")

# DK5: Cow milk and soy milk associated to kiwis give a bitter taste.
dk &= FormulaManager.parser("((cowMilk | soyMilk) & kiwi) -> bitter")

# DK6: A milkshake is a dessert and a dessert must not be bitter.
dk &=  FormulaManager.parser("(milkshake -> dessert) & (dessert -> ~bitter)")

# DK7: Relations between propositional variables and numerical variables.
dk &=  (PropositionalVariable("banana") // ~LinearConstraint("banana_g <= 0"))\
     & (PropositionalVariable("kiwi") // ~LinearConstraint("kiwi_g <= 0"))\
     # & (PropositionalVariable("cowMilk") // ~LinearConstraint("cowMilk_g <= 0"))\
     # & (PropositionalVariable("soyMilk") // ~LinearConstraint("soyMilk_g <= 0"))\
     # & (PropositionalVariable("almondMilk") // ~LinearConstraint("almondMilk_g <= 0"))\

# DK8: The number of types of fruits must be constant before and after the adaptation.
dk &= LinearConstraint("nb_fruitTypes - b2i_banana - b2i_kiwi = 0")

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case
src =  LinearConstraint("banana_u = 2")\
     & LinearConstraint("granulatedSugar_tbsp = 4")\
     & LinearConstraint("vanillaSugar_u = 2")\
     & LinearConstraint("cowMilk_L = 1.")\
     & LinearConstraint("iceCube_u = 4")\
     & LinearConstraint("kiwi_g = 0.")\
     & LinearConstraint("soyMilk_g = 0.")\
     & LinearConstraint("almondMilk_g = 0.")\
     & PropositionalVariable("milkshake")\

# Target problem
tgt = FormulaManager.parser("kiwi & milkshake")

res = adaptator.execute(src, tgt, dk)[1]