from .NaryFormula import NaryFormula
# local import of Or

class And(NaryFormula):
    
    _symbol = "AND"
    
    def toDNF(self):
        
        from .Or import Or
        
        dnfChildren = {child.toDNF() for child in self._children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, Or):		
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren ^ orChildren
        
        if not orChildren:
            return Or(dnfChildren)
        
        combinations = {orChild for orChild in orChildren.pop()._children}
	
        tempcomb = set() 
        for orChild in orChildren:
            for elem in orChild._children:
                for comb in combinations:
                    tempc = comb.copy() 
                    tempcomb.add(tempc.add(elem))
        combinations = tempc

        dnfFormula = {dnfChildren.union(And(comb)) for comb in combinations}
					
        return Or(dnfFormula)
    
    def _toDNFNeg(self):
        
        from .Or import Or
        
        return Or({child._toDNFNeg() for child in self._children})
    
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