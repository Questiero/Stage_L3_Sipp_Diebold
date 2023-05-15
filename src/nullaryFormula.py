import formula
#local import of Not

class NullaryFormula(formula.Formula):
    '''
    Abstract class, representing a Node with an arity of 0, i.e. without 
    any children.

    Attributes
    ----------
    children: None
        The children of the current node. Since there isn't any, it's None.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''
    
    children = None
    
    def toDNF(self) -> formula.Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.
        Since the arity is null, returns self.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form. Since the arity
            is null, returns self.
        '''
        
        return self
    
    def _toDNFNeg(self) -> formula.Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().
        Since the arity is null, returns Not(self).

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation. Since
            the arity is null, returns Not(self).
        '''
        import notOperator

        return notOperator.Not(self)