from formula import Formula

class FormulaManager():

    formulaDict: dict[str, Formula] = dict()

    @staticmethod
    def declare(name: str, formul: Formula) -> Formula:
        FormulaManager.formulaDict[name] = formul
        return formul

    @staticmethod
    def getFormula(name: str) -> Formula:
        return FormulaManager.formulaDict[name]
