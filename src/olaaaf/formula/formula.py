"""
Abstract Formula class, representing a Formula in PCMLC as a syntax tree.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# Typing only imports
from ..variable.variable import Variable
# import constraint

class Formula(ABC):
    '''
    Abstract Formula class, representing a Formula in PCMLC as a syntax tree.

    Attributes
    ----------
    children: 
        The children of the current node.
        Typing depends of the formula's arity.
    '''
    
    children = None
    
    @abstractmethod
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcively returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        set of src.olaaaf.variable.variable.Variable
            All the variables used in the `src.olaaaf.formula.formula.Formula`.
        '''
        pass
    
    @abstractmethod
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        src.olaaaf.formula.formula.Formula
            The current `src.olaaaf.formula.formula.Formula` in Disjunctive Normal Form.
        '''
        pass
    
    @abstractmethod
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        src.olaaaf.formula.formula.Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        pass

    @abstractmethod
    def getAdherence(self, var : Variable = None) -> list[list[Formula]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : src.olaaaf.variable.variable.Variable
            variable used in case of inequality

        Returns
        -------
        list of list of src.olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        pass

    @abstractmethod
    def _getAdherenceNeg(self, var : Variable = None)  -> list[list[Formula]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : src.olaaaf.variable.variable.Variable
            `src.olaaaf.variable.variable.Variable` used in case of inequality

        Returns
        -------
        list of list of src.olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        pass
    
    @abstractmethod
    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `src.olaaaf.formula.formula.Formula` into another one, with only `src.olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        src.olaaaf.formula.formula.Formula
            A `src.olaaaf.formula.formula.Formula` with only `src.olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        pass

    @abstractmethod
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `src.olaaaf.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Returns
        -------
        src.olaaaf.formula.formula.Formula
            A `src.olaaaf.formula.formula.Formula` in the PCMLC formalism.
        '''
        pass

    @abstractmethod
    def _toPCMLCNeg(self, varDict) -> Formula:
        pass
        
    def clone(self) -> Formula:
        """
        Method returning a clone of the current Formula.

        Returns
        -------
        src.olaaaf.formula.formula.Formula
            Clone of the current `src.olaaaf.formula.formula.Formula`.
        """

        clone = self.__class__(self.children)
        return clone
    
    def __eq__(self, o) -> bool:
    
        if o.__class__ != self.__class__:
            return False
        else:
            return self.children == o.children
        
    def __hash__(self):
        return hash(frozenset(self.children))
    
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def toLatex(self) -> str:
        r"""
        Method returning a \(\LaTeX\) expression representing the Formula. Operators are customisable in `src.olaaaf.constants.Constants`.
        
        Returns
        -------
        String
            The \(\LaTeX\) expression representing the Formula.
        """

        pass
    
    def __or__(self, a):
        from .naryFormula.orOperator import Or
        return Or(self, a)    
    
    def __and__(self, a):
        from .naryFormula.andOperator import And
        return And(self, a)
    
    def __invert__(self):
        from .unaryFormula.notOperator import Not
        return Not(self)

    def __floordiv__(self, a):
        from .binaryFormula.equivalenceOperator import Equivalence
        return Equivalence(self, a)
    
    def __ne__(self, a):
        from .binaryFormula.xorOperator import Xor
        return Xor(self, a)
    
    def __rshift__(self, a):
        from .binaryFormula.implicationOperator import Implication
        return Implication(self, a)