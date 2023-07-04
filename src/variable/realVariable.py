r"""
Class representing a real number Variable, meaning a number \(x \in \mathbb{R}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class RealVariable(Variable):
    r"""
    Class, representing a real number `src.variable.variable.Variable`, meaning a `src.variable.variable.Variable` defined in \(\mathbb{R}\).
    Most of the time, you **shouldn't** use the constructor
    of `src.variable.realVariable.RealVariable` and should rather look into `src.variable.realVariable.RealVariable.declare`, 
    `src.variable.realVariable.RealVariable.declareBulk` or `src.variable.realVariable.RealVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `src.variable.realVariable.RealVariable`.
    """

    def haveBound(self) -> tuple[bool, bool]:
        r"""
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
        r"""
        Method use to known bounds of the variables

        Returns
        -------
        res: 
            can be None, None if the variable have no limits,
            or Fraction, Fraction.
        """

        return None, None
    
    def isInteger(self) -> bool:
        r"""
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have intergers values
            else False
        """

        return False