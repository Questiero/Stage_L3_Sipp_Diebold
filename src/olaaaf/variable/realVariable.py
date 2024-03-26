r"""
Class representing a real number Variable, meaning a number \(x \in \mathbb{R}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class RealVariable(Variable):
    r"""
    Class, representing a real number `src.olaaaf.variable.variable.Variable`, meaning a `src.olaaaf.variable.variable.Variable` defined in \(\mathbb{R}\).
    Most of the time, you **shouldn't** use the constructor
    of `src.olaaaf.variable.realVariable.RealVariable` and should rather look into `src.olaaaf.variable.realVariable.RealVariable.declare`, 
    `src.olaaaf.variable.realVariable.RealVariable.declareBulk` or `src.olaaaf.variable.realVariable.RealVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `src.olaaaf.variable.realVariable.RealVariable`.
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

        return False