"""
Created on Thu Apr 20 11:03:01 2023

@author: questiero
"""
from Variable import Variable
from VariableManager import VariableManager
class IntegerVariable(Variable):
    def __init__(self, name):
        self._name = name

    def declare(name):
        new = IntegerVariable(name)
        VariableManager.add(new)
        return new