import naryFormula
# local import of Or

class And(naryFormula.NaryFormula):
    
    _symbol = "AND"
    
    def toDNF(self):
        
        import orOperator
        
        dnfChildren = {child.toDNF() for child in self._children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, orOperator.Or):		
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren ^ orChildren
        
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
    
    def _toDNFNeg(self):
        
        import orOperator
        
        return orOperator.Or({child._toDNFNeg() for child in self._children})
    
    def getConstraintGonfle(self):
        res = []
        for children in self._children:
            for reschildren in children.getConstraintGonfle():
                for constraint in reschildren:  
                    res.append(constraint)
        return [res]
    
    def getConstraintGonfleNeg(self):
        res = []
        for children in self._children:
            for reschildren in children.getConstraintGonfleNeg():
                res.append(reschildren)
        return res