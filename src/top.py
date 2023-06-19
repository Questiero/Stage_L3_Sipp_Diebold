from .nullaryFormula import NullaryFormula

from .constants import Constants

# Typing only imports
from .variable import Variable
from .constraint import Constraint

class Top(NullaryFormula):
    '''
    Class representing the Top constant.

    Attributes
    ----------
    children: None 
        The children of the current node.
    _symbol: str
        The symbol used to represent Top syntaxically.
    '''
     
    def __init__(self):
        raise NotImplementedError(self.__class__.__name__ + ' is not yet implemented') 
    
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        Top, so None.

        Returns
        -------
        variables: None
            All the variables used in Top, so None.
        '''
        
        return None
    
    def getAdherence(self) ->list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        Top, in Disjunctive Normal Form. In this case, an empty list.

        Returns
        -------
        variables: list of list of Constraint
            2D list containing all the constraints of the adherence of Top,
            in Disjunctive Normal Form. In this case, an empty list.
        '''
        
        return []
    
    def _getAdherenceNeg(self) -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of Top, used when a Negation is in play
        instead of getAdherence(). In this case, an empty list.

        Returns
        -------
        variables: list of list of Constraint
            2D list containing all the constraints of the adherence of Top,
            in Disjunctive Normal Form under Negation. In this case, an empty list. 
        '''
        
        return []
    
    def __str__(self):
        return Constants.TOP_STRING_OPERATOR
    
    def toLatex(self):
        return Constants.TOP_LATEX_OPERATOR