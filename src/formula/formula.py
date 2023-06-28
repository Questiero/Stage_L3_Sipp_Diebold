from __future__ import annotations # used to type hint the class itself

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
    formulaDict: dict[str, Formula] = dict()
    
    @abstractmethod
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        pass
    
    @abstractmethod
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        pass
    
    @abstractmethod
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        pass

    @abstractmethod
    def getAdherence(self, var : Variable) -> list[list[Formula]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        pass

    @abstractmethod
    def _getAdherenceNeg(self, var : Variable)  -> list[list[Formula]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Returns
        -------
        res: list of list of constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        pass
    
    @abstractmethod
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        pass
        
    def clone(self) -> Formula:
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
    def toLatex(self):
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