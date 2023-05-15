import nullaryFormula

# Typing only imports
import variable
import constraint

class Bottom(nullaryFormula.NullaryFormula):
    '''
    Class representing the Bottom constant.

    Attributes
    ----------
    children: None 
        The children of the current node.
    _symbol: str
        The symbol used to represent Bottom syntaxically.
    '''
    
    symbol = "BOT"
    
    def getVariables(self) -> set[variable.Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        Bottom, so None.

        Returns
        -------
        variables: None
            All the variables used in Bottom, so None.
        '''
        
        return None
    
    def getAdherence(self) -> list[list[constraint.Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        Bottom, in Disjunctive Normal Form. In this case, an empty list.

        Returns
        -------
        variables: list of list of Constraint
            2D list containing all the constraints of the adherence of Bottom,
            in Disjunctive Normal Form. In this case, an empty list.
        '''
        
        return []
    
    def _getAdherenceNeg(self) -> list(list(constraint.Constraint)):
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of Bottom, used when a Negation is in play
        instead of getAdherence(). In this case, an empty list.

        Returns
        -------
        variables: list of list of Constraint
            2D list containing all the constraints of the adherence of Bottom,
            in Disjunctive Normal Form under Negation. In this case, an empty list. 
        '''
        
        return []
    
    def __str__(self):
        return self._symbol;