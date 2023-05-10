from __future__ import annotations # used to type hint the class itself

from abc import ABC, abstractmethod

class Variable(ABC):
    '''
    Abstract Variable class.

    Attributes
    ----------
    name: str
        The name of the Variable
    '''
    
    name : str = ""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def declare(name : str) -> Variable:
        '''
        Function used to declare a new variable.
        If this variable already exist and have another type compared to the new declaraton,
        This function will raise an Exception.

        Attributes
        ----------
        String: name
            The name of the Variable to be declared.

        Returns
        -------
        Variable: variable
            The defined variable.
        '''

        pass
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.getName() == other.name
        return False
    
    def __hash__(self) -> int:
        return self.name.__hash__()