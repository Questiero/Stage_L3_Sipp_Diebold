from __future__ import annotations # used to type hint the class itself

from abc import ABC, abstractmethod

# Typing only imports
import variable
import constraint

class Formula(ABC):
    '''
    Abstract Formula class, representing a Formula in PCMLC as a syntax tree.

    Attributes
    ----------
    _children: 
        The children of the current node.
        Typing depends of the formula's arity.
    _symbol: str
        The symbol used to represent the operator syntaxically.
    '''
    
    _children = None
    
    @staticmethod
    def parser(string: str):
        '''
        Static method, allowing to parse a formula from a String

        Attributes
        ----------
        string: String 
            The String to parse
        '''
        
        raise NotImplementedError("Function declare not implemented")
    
    @property
    @abstractmethod
    def _symbol(self) -> str:
        pass
    
    @abstractmethod
    def getVariables(self) -> set[variable.Variable]:
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
    def getAdherence(self) -> list[list[constraint.Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        pass

    @abstractmethod
    def _getAdherenceNeg(self)  -> list[list[constraint.Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    def __or__(self, a):
        import orOperator
        return orOperator.Or(self, a)    
    
    def __and__(self, a):
        import andOperator
        return andOperator.And(self, a)
    
    def __invert__(self):
        import notOperator
        return notOperator.Not(self)

'''
    def __eq__(self, a):
        import biconditionalOperator
        return biconditionalOperator.Biconditional(self, a)
    
    def __ne__(self, a):
        import xorOperator
        return xorOperator.Xor(self, a)
    
    def __rshift__(self, a):
        import implicationOperator
        return implicationOperator.Implication(self, a)
'''