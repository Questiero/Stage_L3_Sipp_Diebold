from src.formula import LinearConstraint, PropositionalVariable, EnumeratedType
from src.mlo_solver import  ScipySolverRounded
from src import Adaptation
from src.variable import RealVariable, IntegerVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans
from src.projector import FloatConvexHullProjector

from fractions import Fraction

k1 = 50 #g/u en moyenne
k2 = 1030 #g/L environ
infinity = 1e6
epsilon = 1e-6

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    PropositionalVariable("lettuce"): Fraction(1),
    PropositionalVariable("escarole"): Fraction(1),
    PropositionalVariable("meat"): Fraction(1),
    PropositionalVariable("greenSalad"): Fraction(1),
    PropositionalVariable("bacon"): Fraction(1),
    PropositionalVariable("vegetarian"): Fraction(1),
    PropositionalVariable("vinegar"): Fraction(1),
    PropositionalVariable("saladDish"): Fraction(1),
    PropositionalVariable("oliveOil"): Fraction(1),
    PropositionalVariable("smokedTofu"): Fraction(1),
    PropositionalVariable("lemonJuice"): Fraction(1),
    PropositionalVariable("salt"): Fraction(1)
}

"""
     INITATIALIZATION OF THE SOLVER
"""

solver = ScipySolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(rounding=10, simplifiers=simplifier)
adaptator = Adaptation(solver, discreteL1DistanceFunction(weights, epsilon=Fraction("1e-4")), simplifier, onlyOneSolution=True, projector=projector)

adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# Règle...
dk =  (PropositionalVariable("lettuce") >> PropositionalVariable("greenSalad"))\
    & (PropositionalVariable("escarole") >> PropositionalVariable("greenSalad"))\
    & ((PropositionalVariable("escarole") | PropositionalVariable("lettuce")) // PropositionalVariable("greenSalad"))\
    & (PropositionalVariable("saladDish") >> PropositionalVariable("greenSalad"))\
    & (PropositionalVariable("vegetarian") >> ~PropositionalVariable("meat"))\
    & (PropositionalVariable("bacon") >> PropositionalVariable("meat"))

# Règles d'adaptation R1 et R2...
ak = (PropositionalVariable("bacon") | PropositionalVariable("smokedTofu"))\
    & ((PropositionalVariable("saladDish") & PropositionalVariable("vinegar")) | (PropositionalVariable("saladDish") & PropositionalVariable("lemonJuice") & PropositionalVariable("salt")))

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case... (variables dans le même ordre que article)
x_src = PropositionalVariable("saladDish")\
    & PropositionalVariable("lettuce")\
    & PropositionalVariable("vinegar")\
    & PropositionalVariable("oliveOil")\
    & PropositionalVariable("bacon")

# Target problem...
y_trgt = PropositionalVariable("saladDish")\
    & ~PropositionalVariable("vinegar")\
    & PropositionalVariable("vegetarian")\
    & ~PropositionalVariable("lettuce")

res = adaptator.execute(x_src, y_trgt, dk & ak)