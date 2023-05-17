from __future__ import annotations # used to type hint the class itself

from variable import Variable
from variableManager import VariableManager

class IntegerVariable(Variable):
    '''
    IntegerVariable class, representing a Variable defined in N.

    Attributes
    ----------
    name: str
        The name of the Variable
    '''
    
    def declare(*lname: str) -> None:
        '''
        Function used to declare a new 
        If this variable already exist and have another type compared to the new declaraton,
        This function will raise an Exception.

        Attributes
        ----------
        String: name
            The name of the Variable to be declared.
        '''
        for name in lname:
            VariableManager.verify(name, IntegerVariable)
        for name in lname:
            VariableManager.add(IntegerVariable(name))
