"""
Created on Thu Apr 20 11:03:01 2023

@author: di3bold
"""
from abc import ABC
class Variable(ABC):
    _name : str = ""

    def __init__(self):
        raise Exception("Variable can't have an instance")

    def getName(self) -> str:
        return self._name