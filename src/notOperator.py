from .unaryFormula import UnaryFormula
from .constants import Constants

# Typing only imports
from .formula import Formula
from .constraint import Constraint
from .variable import Variable

class Not(UnaryFormula):
    '''
    Class representing the Not operator.

    Attributes
    ----------
    children: Formula
        The child of the current node.
    _symbol: str
        The symbol used to represent the node syntaxically.
    '''
        
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self.children._toDNFNeg()
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self.children.toDNF()
    
    def getAdherence(self, var : Variable) -> list[list[Constraint]]:
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
        
        return self.children._getAdherenceNeg(var)
    
    def _getAdherenceNeg(self, var : Variable)  -> list[list[Constraint]]:
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
        
        return self.children.getAdherence(var)
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        return Not(self.children.toLessOrEqConstraint())
    
    def copyNegLitteral(self, e : Variable) -> Constraint:
        
        if not isinstance(self.children, Constraint):
            raise TypeError("This method can only be called on a litteral")
                
        copyNeg = self.children.clone()

        for key in copyNeg.variables:
            copyNeg.variables[key] = -copyNeg.variables[key]
        copyNeg.variables[e] = 1
        copyNeg.bound = -copyNeg.bound
                
        return copyNeg
    
    def __str__(self):
        return Constants.NOT_STRING_OPERATOR + "(" + str(self.children) + ")"
    
    def toLatex(self):
        return Constants.NOT_LATEX_OPERATOR + "(" + self.children.toLatex + ")"