import naryFormula
# local import of And

# Typing only imports
import formula
import constraint
import variable

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
    children: set(Formula) 
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
        
        return Or(formulaSet = {child.toDNF() for child in self.children})
    
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
        
        dnfChildren = {child._toDNFNeg() for child in self.children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, Or):		
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren - orChildren
                
        if len(orChildren) == 0:
            return andOperator.And(formulaSet = dnfChildren)
					
        combinations = [{orChild} for orChild in orChildren.pop().children]
	
        tempcomb = []
        for orChild in orChildren:
            for elem in orChild.children:
                for comb in combinations:
                    tempc = comb.copy()
                    tempc.add(elem)
                    tempcomb.append(tempc)
            combinations = tempcomb
            tempcomb = []

        dnfFormula = [andOperator.And(formulaSet=comb.union(dnfChildren)) for comb in combinations]
            
        return Or(formulaSet = set(dnfFormula))
    
    def getAdherence(self, var : variable.Variable) -> list[list[constraint.Constraint]]:
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
        
        res = []
        
        for children in self.children:
            for reschildren in children.getAdherence(var):
                res.append(reschildren)
                
        return res
    
    def _getAdherenceNeg(self, var : variable.Variable)  -> list[list[constraint.Constraint]]:
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
        
        res = []
        
        for children in self.children:
            for reschildren in children._getAdherenceNeg(var):
                for const in reschildren:  
                    res.append(const)
                    
        return [res]