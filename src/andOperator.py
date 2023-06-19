from .naryFormula import NaryFormula
from .constants import Constants
# local import of Or

# Typing only imports
from .formula import Formula
from .constraint import Constraint
from .variable import Variable

class And(NaryFormula):
    '''
    Class representing the And operator as a relation with an arity equal or
    greater than 2 in PCMLC as a syntax tree.

    Parameters
    ----------
    *formulas: Formula
        The formulas meant as components of the And operator.

    Attributes
    ----------
    children: set[Formula]
        The children of the current node.
    _symbol: str
        The symbol used to represent the And operator syntaxically.
    '''
    
    _symbol = "AND"
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
                
        from .orOperator import Or
        
        dnfChildren = {child.toDNF() for child in self.children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, Or):
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren - orChildren
                
        if len(orChildren) == 0:
            return And(formulaSet = dnfChildren)
        
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
                
        dnfFormula = [And(formulaSet=comb.union(dnfChildren)) for comb in combinations]
            
        #print(dnfFormula)
        return Or(formulaSet = set(dnfFormula))
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        from .orOperator import Or
        
        return Or(formulaSet = {child._toDNFNeg() for child in self.children})
    
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
        
        res = []
        
        for children in self.children:
            for reschildren in children.getAdherence(var):
                for const in reschildren:  
                    res.append(const)
                    
        return [res]
    
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
        
        res = []
        
        for children in self.children:
            for reschildren in children._getAdherenceNeg(var):
                res.append(reschildren)
                
        return res

    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        childrenModified = set()
        
        for child in self.children:
            childrenModified.add(child.toLessOrEqConstraint())

        return And(formulaSet = childrenModified)
    
    def __str__(self):

        symbol = Constants.AND_STRING_OPERATOR

        if len(self.children) == 1:
            return str(list(self.children)[0])
        
        s = ""
        for child in self.children:
            s += "(" + str(child) + ") " + symbol + " "
        toRemove = len(symbol) + 2
        s = s[:-toRemove] + ""
        return s
    
    def toLatex(self):

        symbol = Constants.AND_LATEX_OPERATOR

        if len(self.children) == 1:
            return list(self.children)[0].toLatex()
        
        s = ""
        for child in self.children:
            s += "(" + child.toLatex() + ") " + symbol + " "
        toRemove = len(symbol) + 2
        s = s[:-toRemove] + ""
        return s