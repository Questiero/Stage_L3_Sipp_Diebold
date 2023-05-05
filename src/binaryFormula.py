import formula

# Typing only imports
import variable

from abc import abstractmethod

class BinaryFormula(formula.Formula):
    '''
    Abstract class, representing a binary operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the binary operator.

    Attributes
    ----------
    _children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''
        
    # formulas: tuple (Formula, Formula)
    def __init__(self, formulaTuple: tuple(formula.Formula, formula.Formula)):
        self._children = formulaTuple

    @abstractmethod
    def _simplify(self) -> formula.Formula:
        '''
        Method returning the simplified form for the binary operator, using only
        Not, And and Or.

        Returns
        -------
        formula: Formula
            The simplified version of the binary operator.
        '''
        
        pass
    
    def getVariables(self) -> set[variable.Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self._children.getVariables()
    
    def toDNF(self) -> formula.Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        variables: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self._simplify().toDNF()
    
    def _toDNFNeg(self) -> formula.Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        variables: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self._simplify()._toDNFNeg()
    
    def __str__(self):
        return str(self._children[0]) + self._symbol + str(self._children[1])