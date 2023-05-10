import naryFormula
# local import of And

# Typing only imports
import formula
import constraint

class Or(naryFormula.NaryFormula):
    '''
    Class representing the Or operator as a relation with an arity equal or
    greater than 2 in PCMLC as a syntax tree.

    Parameters
    ----------
    *formulas: Formula
        The formulas meant as components of the Or operator.

    Attributes
    ----------
    _children: set(Formula) 
        The children of the current node.
    _symbol: str
        The symbol used to represent the Or operator syntaxically.
    '''
    
    _symbol = "OR"
    
    def toDNF(self) -> formula.Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return Or(formulaSet = {child.toDNF() for child in self._children})
    
    def _toDNFNeg(self) -> formula.Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        import andOperator
        
        dnfChildren = {child._toDNFNeg() for child in self._children}
			
        andChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, andOperator.And):		
                andChildren.add(dnfChild)

        dnfChildren = dnfChildren - andChildren
                
        if not andChildren:
            return Or(formulaSet = dnfChildren)
					
        combinations = {andChild for andChild in andChildren.pop().__children}
	
        tempcomb = set() 
        for andChild in andChildren:
            for elem in andChild._children:
                for comb in combinations:
                    tempc = comb.copy() 
                    tempcomb.add(tempc.add(elem))
        combinations = tempc

        dnfFormula = {dnfChildren.union(andOperator.And(comb)) for comb in combinations}
					
        return Or(formulaSet = dnfFormula)
    
    def getAdherence(self)  -> list[list[constraint.Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Returns
        -------
        res: list of list of Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        
        res = []
        
        for children in self._children:
            for reschildren in children.getConstraintGonfle():
                res.append(reschildren)
                
        return res
    
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
        
        res = []
        
        for children in self._children:
            for reschildren in children.getConstraintGonfleNeg():
                for const in reschildren:  
                    res.append(const)
                    
        return [res]