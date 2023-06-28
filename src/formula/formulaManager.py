from .formula import Formula
from pyparsing import Literal, Word, srange, infix_notation, OpAssoc, ParseResults, ParserElement
from ..constants import Constants

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
        ParserElement.enablePackrat()
        
        formWord = Word(srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_]"))

        expr = infix_notation(formWord,
                              [(Literal(Constants.AND_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.OR_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.NOT_PARSER_OPERATOR), 1, OpAssoc.RIGHT),
                               (Literal(Constants.IMPLICATION_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.XOR_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.EQUIVALENCE_PARSER_OPERATOR), 2, OpAssoc.LEFT)],
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
                if(tokens[0] == Constants.NOT_PARSER_OPERATOR):
                    from .unaryFormula.notOperator import Not
                    return Not(FormulaManager.__parserEvaluator(tokens[1]))
            elif(len(tokens) % 2 == 1):
                
                formulaType = None

                match tokens[1]:

                    case Constants.AND_PARSER_OPERATOR:
                        from .naryFormula.andOperator import And
                        formulaType = And
                    case Constants.OR_PARSER_OPERATOR:
                        from .naryFormula.orOperator import Or
                        formulaType = Or
                    case Constants.XOR_PARSER_OPERATOR:
                        from .binaryFormula.xorOperator import Xor
                        formulaType = Xor
                    case Constants.IMPLICATION_PARSER_OPERATOR:
                        from ..implicationOperator import Implication
                        formulaType = Implication
                    case Constants.EQUIVALENCE_PARSER_OPERATOR:
                        from .binaryFormula.equivalenceOperator import Equivalence
                        formulaType = Equivalence

                return formulaType(FormulaManager.__parserEvaluator(tokens[0]), FormulaManager.__parserEvaluator(tokens[2:]))

            else:
                raise TypeError("oop")
                
        elif isinstance(tokens, str):

            return FormulaManager.getFormula(tokens)

    @staticmethod
    def declare(name: str, formul: Formula) -> Formula:
        FormulaManager.formulaDict[name] = formul
        return formul

    @staticmethod
    def getFormula(name: str) -> Formula:
        return FormulaManager.formulaDict[name]
