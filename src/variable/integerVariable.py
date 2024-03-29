r"""
Class representing an integer number Variable, meaning a number \(x \in \mathbb{Z}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class IntegerVariable(Variable):
    r"""
    Class, representing an integer number `src.variable.variable.Variable`, meaning a `src.variable.variable.Variable` defined in \(\mathbb{Z}\).
    Most of the time, you **shouldn't** use the constructor
    of `src.variable.integerVariable.IntegerVariable` and should rather look into `src.variable.integerVariable.IntegerVariable.declare`, 
    `src.variable.integerVariable.IntegerVariable.declareBulk` or `src.variable.integerVariable.IntegerVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `src.variable.integerVariable.IntegerVariable`.
    """

    def haveBound(self) -> tuple[bool, bool]:
        """
        Method use to say if the variable have lower and upper bound

        Returns
        -------
        res: 
            true,true if the variable have a lower and an upper bound
            true, false if the variable have a lower and not an upper bound
            etc...
        """

        return False, False

    def getBounds(self) -> tuple[Fraction, Fraction]:
        """
        Method use to known bounds of the variables

        Returns
        -------
        res: 
            can be None, None if the variable have no limits,
            or Fraction, Fraction.
        """

        return None, None

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