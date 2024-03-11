from . import PropositionalVariable

from itertools import combinations

class EnumeratedType:

    name: str
    values: dict[str, PropositionalVariable]
    __instances = {}

    def __init__(self, name: str, values: list[str] = None):
        
        #TODO verif au moins 2 éléments
        self.values = {val:PropositionalVariable("e2b_" + name + ":" + val) for val in values}
        self.name = name

    @staticmethod
    def declare(name: str, values: list[str]):
        
        newType = EnumeratedType(name, values)
        __class__.__instances[name] = newType

        return newType
    
    @staticmethod
    def get(name: str):
        return __class__.__instances[name]

    def __getitem__(self, key: str):

        # TODO check erreur
        return self.values[key]
    
    def generateConstraints(self):

        from ...naryFormula import And, Or

        propSet = self.values.values()
        
        constraints = Or(*propSet)

        for propTuple in combinations(propSet, len(propSet)-1):
            constraints &= ~And(*propTuple)

        return constraints