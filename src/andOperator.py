import naryFormula
# local import of Or

# Typing only imports
import formula
import constraint

class And(naryFormula.NaryFormula):
    '''
    Class representing the And operator as a relation with an arity equal or
    greater than 2 in PCMLC as a syntax tree.

    Parameters
    ----------
    *formulas: Formula
        The formulas meant as components of the And operator.

    Attributes
    ----------
    _children: set[Formula]
        The children of the current node.
    _symbol: str
        The symbol used to represent the And operator syntaxically.
    '''
    
    _symbol = "AND"
    
    def toDNF(self) -> formula.Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        import orOperator
        
        dnfChildren = {child.toDNF() for child in self._children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, orOperator.Or):		
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren - orChildren
        
        if not orChildren:
            return orOperator.Or(dnfChildren)
        
        combinations = {orChild for orChild in orChildren.pop()._children}
	
        tempcomb = set() 
        for orChild in orChildren:
            for elem in orChild._children:
                for comb in combinations:
                    tempc = comb.copy() 
                    tempcomb.add(tempc.add(elem))
        combinations = tempc

        dnfFormula = {dnfChildren.union(And(comb)) for comb in combinations}
					
        return orOperator.Or(dnfFormula)
    
    def _toDNFNeg(self) -> formula.Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        import orOperator
        
        return orOperator.Or({child._toDNFNeg() for child in self._children})
    
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
        
        res = []
        
        for children in self._children:
            for reschildren in children.getConstraintGonfle():
                for const in reschildren:  
                    res.append(const)
                    
        return [res]
    
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
        
        res = []
        
        for children in self._children:
            for reschildren in children.getConstraintGonfleNeg():
                res.append(reschildren)
                
        return res