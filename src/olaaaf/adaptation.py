r"""
Main class of the module, allowing the user to make the adaptation between two `src.olaaaf.formula.formula.Formula`
\(src\) and \(tgt\) that are constraints.
"""

from __future__ import annotations

from .formula import Formula
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .revision import Revision

class Adaptation:
    r"""
    Main class of the module, allowing the user to make the adaptation between two `src.olaaaf.formula.formula.Formula`
    \(src\) and \(tgt\) that are constraints.

    Parameters
    ----------
    solverInit : src.olaaaf.mlo_solver.MLOSolver.MLOSolver
        The solver that will be used for optimization.
    distance : src.olaaaf.distance.distance_function.distanceFunction.DistanceFunction
        The distance function that will be used and, more importantly, the weights \((w_i)\) and \(\varepsilon\) arguments of it.
        The original algorithm is meant to be used with a `src.olaaaf.distance.distance_function.discreteL1DistanceFunction.discreteL1DistanceFunction`.
    simplifiers : list of src.olaaaf.simplificator.simplificator.Simplificator, optional
        List of all of the `src.olaaaf.simplificator.simplificator.Simplificator` that will be applied to the `src.olaaaf.formula.formula.Formula`, 
        in order given by the list.
    onlyOneSolution : boolean, optional
        If set to `True`, the adaptation algorithm will only return one point that satisfies \(\psi \circ \mu\).
        If not, it will return all solutions.
        By default, this constant is set to whichever one was chosen in `src.olaaaf.constants.Constants`.
    verbose : boolean, optional
        If set to `True`, the adaptation algorithm will have a verbose display in the terminal.
        By default, this constant is set to whichever one was chosen in `src.olaaaf.constants.Constants`.
    projector : boolean, optional
        Projector algorithm to use, only necessary if `onlyOneSolution` is set to `False`.
    """

    __revision : Revision

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, verbose: bool = Constants.SET_VERBOSE, projector: Projector = None) -> None:        
        
        self.__revision = Revision(solverInit, distance, simplifiers, onlyOneSolution, verbose, projector)

    def preload(self):
        r"""
        Methd used to preload the adaptation algorithm.

        This step is necessary before using `execute` and recommended before the domain knowledge definition since it translates every
        non-`src.olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` into one and introduces new under-the-box variables that the user might want to use.
        """

        self.__revision.preload()

    def execute(self, src : Formula, trgt : Formula, dk : Formula):
        r"""
        Execute the adaptation of \(src\) by \(tgt\), with the domain knowledge \(DK\).

        Parameters
        ----------
        psi : src.olaaaf.formula.formula.Formula
            \(src\), source case for the adaptation and `src.olaaaf.formula.formula.Formula` that will be adapted.
        mu : src.olaaaf.formula.formula.Formula
            \(tgt\), target problem for the adaptation and `src.olaaaf.formula.formula.Formula` that will be used to adapt \(src\) by.
        dk : src.olaaaf.formula.formula.Formula
            \(DK\), the domain knowledge.

        Returns
        -------
        Fraction
            Distance (calculated with the `src.olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) between \(src\) and \(tgt\).
        src.olaaaf.formula.formula.Formula
            Result of the adaptation of \(src\) by \(tgt\).
        """

        return self.__revision.execute(src & dk, trgt & dk)