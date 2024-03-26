r"""
Class representing an integer number Variable, meaning a number \(x \in \mathbb{Z}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class IntegerVariable(Variable):
    r"""
    Class, representing an integer number `src.olaaaf.variable.variable.Variable`, meaning a `src.olaaaf.variable.variable.Variable` defined in \(\mathbb{Z}\).
    Most of the time, you **shouldn't** use the constructor
    of `src.olaaaf.variable.integerVariable.IntegerVariable` and should rather look into `src.olaaaf.variable.integerVariable.IntegerVariable.declare`, 
    `src.olaaaf.variable.integerVariable.IntegerVariable.declareBulk` or `src.olaaaf.variable.integerVariable.IntegerVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `src.olaaaf.variable.integerVariable.IntegerVariable`.
    """

    def isInteger(self) -> bool:
        """
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have intergers values
            else False
        """

        return True