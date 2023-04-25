from .NaryFormula import NaryFormula
from .Or import Or

class And(NaryFormula):
    
    _symbol = "AND"
    
    def toDNF(self):
        dnfChildren = {child.toDNF() for child in self._children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, Or):		
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
					
        return Or(dnfFormula)
    
    def _toDNFNeg(self):
        return Or({child._toDNFNeg() for child in self._children})