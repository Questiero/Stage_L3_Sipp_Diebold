"""
Abstract class, representating a projector of a `src.olaaaf.formula.formula.Formula` to a subset of its `src.olaaaf.variable.variable.Variable`.
"""

from __future__ import annotations

from ..formula import Formula, And
from ..variable import Variable

from abc import ABC, abstractmethod

class Projector (ABC):

    @abstractmethod
    def projectOn(self, phi: And, variables: set[Variable]) -> Formula:
        r"""
        Main method of `src.olaaaf.projector.projector.Projector`, allowing to project a given `src.olaaaf.formula.formula.Formula`
        to a subset of its `src.olaaaf.variable.variable.Variable`.

        Parameters
        ----------
        phi: src.olaaaf.formula.formula.Formula
            The `src.olaaaf.formula.formula.Formula` to project.
        variables: set of src.olaaaf.variable.variable.Variable
            The subset of `src.olaaaf.variable.variable.Variable` to project on.
        
        Returns
        -------
        src.olaaaf.formula.formula.Formula
            The projection of \(\varphi\) on the specified subset of its variables.
        """
        pass