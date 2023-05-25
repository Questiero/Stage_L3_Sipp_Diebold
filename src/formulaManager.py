from formula import Formula
from pyparsing import Literal, Word, srange, infix_notation, OpAssoc, ParseResults
from notOperator import Not
from andOperator import And
from orOperator import Or
from xorOperator import Xor
from implicationOperator import Implication
from equivalenceOperator import Equivalence
from constants import Constants

class FormulaManager():

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
                              [(Literal(Constants.AND_OPERATOR_PARSER), 2, OpAssoc.LEFT),
                               (Literal(Constants.OR_OPERATOR_PARSER), 2, OpAssoc.LEFT),
                               (Literal(Constants.NOT_OPERATOR_PARSER), 1, OpAssoc.RIGHT),
                               (Literal(Constants.IMPLICATION_OPERATOR_PARSER), 2, OpAssoc.LEFT),
                               (Literal(Constants.XOR_OPERATOR_PARSER), 2, OpAssoc.LEFT),
                               (Literal(Constants.EQUIVALENCE_OPERATOR_PARSER), 2, OpAssoc.LEFT)],
                              lpar = "(",
                              rpar = ")")

        tokens = expr.parse_string(string)

        #return tokens
        return FormulaManager.__parserEvaluator(tokens)
    
    @staticmethod
    def __parserEvaluator(tokens: ParseResults) -> Formula:

        if isinstance(tokens, ParseResults) or isinstance(tokens, list):

            if(len(tokens) == 1):
                return FormulaManager.__parserEvaluator(tokens[0])
            elif(len(tokens) == 2):
                if(tokens[0] == Constants.NOT_OPERATOR_PARSER):
                    return Not(FormulaManager.__parserEvaluator(tokens[1]))
            elif(len(tokens) % 2 == 1):
                
                formulaType = None

                match tokens[1]:

                    case Constants.AND_OPERATOR_PARSER:
                        formulaType = And
                    case Constants.OR_OPERATOR_PARSER:
                        formulaType = Or
                    case Constants.XOR_OPERATOR_PARSER:
                        formulaType = Xor
                    case Constants.IMPLICATION_OPERATOR_PARSER:
                        formulaType = Implication
                    case Constants.EQUIVALENCE_OPERATOR_PARSER:
                        formulaType = Equivalence

                return formulaType(FormulaManager.__parserEvaluator(tokens[0]), FormulaManager.__parserEvaluator(tokens[2:]))

            else:
                raise TypeError("oop")
                
        elif isinstance(tokens, str):

            from formulaManager import FormulaManager

            return FormulaManager.getFormula(tokens)

    @staticmethod
    def declare(name: str, formul: Formula) -> Formula:
        FormulaManager.formulaDict[name] = formul
        return formul

    @staticmethod
    def getFormula(name: str) -> Formula:
        return FormulaManager.formulaDict[name]
