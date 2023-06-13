from formula import Formula

# Typing only imports
from variable import Variable
from constraint import Constraint

from abc import abstractmethod

class BinaryFormula(Formula):
    '''
    Abstract class, representing a binary operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the binary operator.

    Attributes
    ----------
    children: tuple of Formulas
        The children of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''
        
    # formulas: tuple (Formula, Formula)
    def __init__(self, formulaLeft: Formula, formulaRight: Formula):
        self.children = (formulaLeft, formulaRight)

    @abstractmethod
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the binary operator, using only
        Not, And and Or.

        Returns
        -------
        formula: Formula
            The simplified version of the binary operator.
        '''
        
        pass
    
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        
        return self.children[0].getVariables().union(self.children[1].getVariables())
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        variables: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self._eliminate().toDNF()
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        variables: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self._eliminate()._toDNFNeg()
    
    def getAdherence(self, var : Variable) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        return self._eliminate().getAdherence(var)

    def _getAdherenceNeg(self, var : Variable)  -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        return self._eliminate()._getAdherenceNeg(var)
    
    def __str__(self):
        return "(" + str(self.children[0]) + ") " + self._symbol +  " (" + str(self.children[1]) + ")"
