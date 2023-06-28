from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class IntegerVariable(Variable):
    '''
    IntegerVariable class, representing a Variable defined in N.

    Attributes
    ----------
    name: str
        The name of the Variable
        Name must begin with an alphabet character. It can be followed by alphanumerical character or _.
        Name can't have this symbole : + - * / @
    '''

    def declare(name: str) -> IntegerVariable:
        '''
        Function used to declare a new 
        If this variable already exist and have another type compared to the new declaraton,
        This function will raise an Exception.

        Attributes
        ----------
        String: name
            The name of the Variable to be declared.
        '''
        return VariableManager.add(IntegerVariable(name))
    
    def declareBulk(*lname: str) -> list[IntegerVariable]:
        '''
        Function used to declare a new 
        If this variable already exist and have another type compared to the new declaraton,
        This function will raise an Exception.

        Attributes
        ----------
        String: name
            The name of the Variable to be declared.
        '''
        vars = []
        for name in lname:
            vars.append(VariableManager.add(IntegerVariable(name)))
        return vars

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
        return False, False

    def getBounds(self) -> tuple[Fraction, Fraction]:
        '''
        Method use to known bounds of the variables

        Returns
        -------
        res: 
            can be None, None if the variable have no limits,
            or Fraction, Fraction.
        '''
        return None, None

    def isInteger(self) -> bool:
        '''
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have intergers values
            else False
        '''
        return True