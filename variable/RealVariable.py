"""
Created on Thu Apr 20 11:03:01 2023

@author: questiero
"""
from Variable import Variable
class RealVariable(Variable):
    def __init__(self, name):
        self._name = name

    def declare(name):
        new = RealVariable(name)
        Variable.add(new)
        return new
    
test = RealVariable.declare("x")
