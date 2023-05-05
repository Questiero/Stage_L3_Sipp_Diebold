import unaryFormula

# Typing only imports
import formula
import constraint

class Not(unaryFormula.UnaryFormula):
    '''
    Class representing the Not operator.

    Attributes
    ----------
    _children: Formula
        The child of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''
    
    _symbol = "!"
    
    def toDNF(self) -> formula.Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self._children._toDNFNeg()
    
    def _toDNFNeg(self) -> formula.Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self._children.toDNF()
    
    def getAdherence(self) -> list[list[constraint.Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        
        return self._children.getConstraintGonfleNeg()
    
    def _getAdherenceNeg(self) -> list[list[constraint.Constraint]]:
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
        
        return self._children.getConstraintGonfle()