from .NaryFormula import NaryFormula
from ..binary import *

class And(NaryFormula):
    
    _symbol = "AND"
    
    def toDNF(self):
        dnfChildren = {child.toDNF() for child in self._children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, binary.Or):		
                orChildren.add(dnfChild)
                dnfChildren.remove(dnfChild)
					
        combinations = {orChild for orChild in orChildren.pop()}
	
        tempcomb = set() 
        for orChild in orChildren:
            for elem in orChild:
                for comb in combinations:
                    tempc = comb.copy() 
                    tempcomb.add(tempc.add(elem))
        combinations = tempc

        dnfFormula = {dnfChildren.union(And(comb)) for comb in combinations}
					
        return binary.Or(dnfFormula)
    
    def _toDNFNeg(self):
        return binary.Or({child._toDNFNeg() for child in self._children})
    
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