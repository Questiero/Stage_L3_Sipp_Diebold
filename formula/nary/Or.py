from .NaryFormula import NaryFormula
from .And import And

class Or(NaryFormula):
    
    _symbol = "OR"
    
    def toDNF(self):
        return Or({child.toDNF() for child in self._children})
    
    def _toDNFNeg(self):
        
        dnfChildren = {child._toDNFNeg() for child in self._children}
			
        andChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, And):		
                andChildren.add(dnfChild)
                dnfChildren.remove(dnfChild)
					
        combinations = {andChild for andChild in andChildren.pop()}
	
        tempcomb = set() 
        for andChild in andChildren:
            for elem in andChild:
                for comb in combinations:
                    tempc = comb.copy() 
                    tempcomb.add(tempc.add(elem))
        combinations = tempc

        dnfFormula = {dnfChildren.union(And(comb)) for comb in combinations}
					
        return Or(dnfFormula)