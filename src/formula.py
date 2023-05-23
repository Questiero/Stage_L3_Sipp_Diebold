from __future__ import annotations # used to type hint the class itself

from abc import ABC, abstractmethod
from pyparsing import Literal, Word, srange, infix_notation, OpAssoc, ParseResults
# local import of andOperator
# local import of orOperator
# local import of notOperator
# local import of xorOperator
# local import of implicationOperator
# local import of equivalenceOperator

# Typing only imports
from variable import Variable
# import constraint

class Formula(ABC):
    '''
    Abstract Formula class, representing a Formula in PCMLC as a syntax tree.

    Attributes
    ----------
    children: 
        The children of the current node.
        Typing depends of the formula's arity.
    _symbol: str
        The symbol used to represent the operator syntaxically.
    '''
    
    children = None
    formulaDict: dict[str, Formula] = dict()
    
    @staticmethod
    def parser(string: str):
        '''
        Static method, allowing to parse a formula from a String

        Attributes
        ----------
        string: String 
            The String to parse
        '''
        
        formWord = Word(srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_]"))

        expr = infix_notation(formWord,
                              [(Literal("&"), 2, OpAssoc.LEFT),
                               (Literal("|"), 2, OpAssoc.LEFT),
                               (Literal("~"), 1, OpAssoc.RIGHT),
                               (Literal("->"), 2, OpAssoc.LEFT),
                               (Literal("<-/->"), 2, OpAssoc.LEFT),
                               (Literal("<->"), 2, OpAssoc.LEFT)],
                              lpar = "(",
                              rpar = ")")

        tokens = expr.parse_string(string)

        #return tokens
        return Formula.__parserEvaluator(tokens)
    
    @staticmethod
    def __parserEvaluator(tokens) -> Formula:

        from notOperator import Not
        from andOperator import And
        from orOperator import Or
        from xorOperator import Xor
        from implicationOperator import Implication
        from equivalenceOperator import Equivalence

        if isinstance(tokens, ParseResults) or isinstance(tokens, list):

            if(len(tokens) == 1):
                return Formula.__parserEvaluator(tokens[0])
            elif(len(tokens) == 2):
                if(tokens[0] == "~"):
                    return Not(Formula.__parserEvaluator(tokens[1]))
            elif(len(tokens) % 2 == 1):
                
                formulaType = None

                match tokens[1]:

                    case "&":
                        print("&")
                        formulaType = And
                    case "|":
                        formulaType = Or
                    case "<-/->":
                        formulaType = Xor
                    case "->":
                        formulaType = Implication
                    case "<->":
                        formulaType = Equivalence

                return formulaType(Formula.__parserEvaluator(tokens[0]), Formula.__parserEvaluator(tokens[2:]))

            else:
                raise TypeError("oop")
                
        elif isinstance(tokens, str):

            from linearConstraint import LinearConstraint
            
            return LinearConstraint("x = 1")
            print(globals())
            tok = globals()[tokens]

            if isinstance(tok, Formula):
                return tok
            else:
                raise TypeError("Oop")
            

    @property
    @abstractmethod
    def _symbol(self) -> str:
        pass
    
    @abstractmethod
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of Variable
            All the variables used in the Formula.
        '''
        pass
    
    @abstractmethod
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form.
        '''
        pass
    
    @abstractmethod
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        formula: Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        pass

    @abstractmethod
    def getAdherence(self, var : Variable) -> list[list[Formula]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        pass

    @abstractmethod
    def _getAdherenceNeg(self, var : Variable)  -> list[list[Formula]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Returns
        -------
        res: list of list of constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        pass
    
    @abstractmethod
    def toLessOrEqConstraint(self):
        '''
        Method used to transforming formula to anoter formula without equality or greater constraint

        Returns
        ------
        res: Formula with only minus or equal constraint
        
        '''
        pass
        
    def clone(self) -> Formula:
        clone = self.__class__(self.children)
        return clone
    
    def __eq__(self, o) -> bool:
    
        if o.__class__ != self.__class__:
            return False
        else:
            return self.children == o.children
        
    def __hash__(self):
        return hash(frozenset(self.children))
    
    @abstractmethod
    def __str__(self):
        pass
    
    def __or__(self, a):
        import orOperator
        return orOperator.Or(self, a)    
    
    def __and__(self, a):
        import andOperator
        return andOperator.And(self, a)
    
    def __invert__(self):
        import notOperator
        return notOperator.Not(self)

    def __floordiv__(self, a):
        import equivalenceOperator
        return equivalenceOperator.Equivalence(self, a)
    
    def __ne__(self, a):
        import xorOperator
        return xorOperator.Xor(self, a)
    
    def __rshift__(self, a):
        import implicationOperator
        return implicationOperator.Implication(self, a)