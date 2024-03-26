"""
Representation of simplification algorithms, used to simplify a conjunction of litterals
(i.e `src.olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
`src.olaaaf.formula.unaryFormula.notOperator.Not`).
"""

from .simplificator import Simplificator
from .caron import Caron
from .daalmans import Daalmans