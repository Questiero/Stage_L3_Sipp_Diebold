"""
Created on Thu Apr 20 11:03:01 2023

@author: Di3bold
"""
from .variable import Variable
from .variableManager import VariableManager

class RealVariable(Variable):
    def __init__(self, name):
        self._name = name

    def declare(name):
        """
            Function used to declare a new variable.
            If this variable already exist and have another type compared to the new declaraton,
            This function will raise an Exception.

            :param name: Name of the new variable
            :returns: A variable
        """
        new = RealVariable(name)
        VariableManager.add(new)
        return new
