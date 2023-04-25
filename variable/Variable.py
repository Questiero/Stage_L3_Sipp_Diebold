"""
Created on Thu Apr 20 11:03:01 2023

@author: di3bold
"""
from abc import ABC
class Variable(ABC):
    instance = {}
    _name = ""

    def __init__(self):
        raise Exception("Variable can't have an instance")