from __future__ import annotations # used to type hint the class itself

from variable import Variable
from variableManager import VariableManager

class RealVariable(Variable):
    '''
    RealVariable class, representing a Variable defined in R.

    Attributes
    ----------
    name: str
        The name of the Variable
    '''
    
    def declare(*lname: str) -> RealVariable:
        '''
        Function used to declare a new 
        If this variable already exist and have another type compared to the new declaraton,
        This function will raise an Exception.

        Attributes
        ----------
        String: name
            The name of the Variable to be declared.

        Returns
        -------
        Variable: variable
            The defined 
        '''
        for name in lname:
            VariableManager.verify(name, RealVariable)
        for name in lname:
            VariableManager.add(RealVariable(name))