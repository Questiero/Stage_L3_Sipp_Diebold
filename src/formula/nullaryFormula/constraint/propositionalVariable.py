"""
Representation of a PropositionalVariable in CPC.
"""

from __future__ import annotations

from . import Constraint
from ...formulaManager import FormulaManager
# Typing only imports
from ....variable.variable import Variable


class PropositionalVariable(Constraint):

    def __init__(self, nameVariable: str, name: str = None):
        self.nameVariable = nameVariable
       # Declare if name
        if(name is not None):
            FormulaManager.declare(name, self)
    
    def getVariables(self):
        '''
        Not applicable here
        '''
        raise NotImplementedError("getVariables cannot be use here, the Formula contains a PropositionalVariable")
    
    def getAdherence(self, var : Variable):
        '''
        Not applicable here
        '''
        raise NotImplementedError("getAdherence cannot be use here, the Formula contains a PropositionalVariable")

    def _getAdherenceNeg(self, var : Variable):
        '''
        Not applicable here
        '''
        raise NotImplementedError("_getAdherenceNeg cannot be use here, the Formula contains a PropositionalVariable")
    
    def __str__(self):

        return self.nameVariable
    
    def toLatex(self):

        return self.nameVariable
            
    def toLessOrEqConstraint(self):
        '''
        Not applicable here
        '''
        raise NotImplementedError("toLessOrEqConstraint cannot be use here, the Formula contains a PropositionalVariable")
    
    def clone(self) -> PropositionalVariable:
        """
        Method returning a clone of the current Formula.

        Returns
        -------
        src.formula.formula.Formula
            Clone of the current `src.formula.formula.Formula`.
        """
                
        clonedPv = PropositionalVariable("")
        clonedPv.nameVariable = self.nameVariable.copy()
        return clonedPv
      
    def __eq__(self, o) -> bool: #BRAVO
        if o.__class__ != self.__class__:
            return False
        else:
            return o.nameVariable == self.nameVariable
        
    def __hash__(self):
        return hash(str(self))


