from __future__ import annotations # used to type hint the class itself
from fractions import Fraction
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

    @classmethod
    def declareAnonymous(cls) -> Variable:
        v = cls("")
        v.name = id(v)
        return v 


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
            Name must begin with an alphabet character. It can be followed by alphanumerical character or _.
            Name can't have this symbole : + - * / @

        Returns
        -------
        Variable: variable
            The defined variable.
        '''

        pass

    @abstractmethod
    def haveBound(self) -> tuple[bool, bool]:
        '''
        Method use to say if the variable have lower and upper bound

        Returns
        -------
        res: 
            true,true if the variable have a lower and an upper bound
            true, false if the variable have a lower and not an upper bound
            etc...
        '''
        pass

    @abstractmethod
    def getBounds(self) -> tuple[Fraction, Fraction]:
        '''
        Method use to known bounds of the variables

        Returns
        -------
        res: 
            can be None, None if the variable have no limits,
            or Fraction, Fraction.
        '''
        pass
    
    @abstractmethod
    def isInteger(self) -> bool:
        '''
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have intergers values
            else False
        '''
        pass


    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False
    
    def __hash__(self) -> int:
        return self.name.__hash__()