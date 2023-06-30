"""
Abstract class, representing a variable.
"""

from __future__ import annotations

from fractions import Fraction
from abc import ABC, abstractmethod

class Variable(ABC):
    '''
    Abstract class, representing a variables.
    '''
    
    #: Name of the variable, by which they are identified.
    name : str = ""

    def __init__(self, name):
        self.name = name

    @classmethod
    def declareAnonymous(cls, ending: str = None) -> Variable:
        """
        Function allowing the user to declar an anonymous variable meant to be used inside algorithms without risking any
        naming conflit with the standardly defined variables.\n
        Anonymous variables aren't stored in `src.variable.variableManager.VariableManager.instance` and, as such,
        can't be used in `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`'s constructor.\n

        Since they can't be used in the usual constructor, one must first declare an empty
        `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` before adding them manualy.

        To prevent naming conflicts with regular variables, an anonymous variable's name always start with
        it's object's id. The user can also specify an ending to an anonymous variable name.

        Attributes
        ----------
        ending: str
            The string to concatenate at the end of an anonymous variable's name, after its object id.

        Usage exemple
        ----------
        ```py
            lc = LinearConstraint("")

            for i in range(5):
                lc.variables[IntegerVariable.declareAnonymous("anonymous")] = 1

            lc.operator = ConstraintOperator.LEQ
            lc.bound = Fraction("5/2")

            print(lc)
            >>> 1949361817056anonymous + 1949361816720anonymous + 1949372682384anonymous + 1949435231104anonymous + 1949435231200anonymous <= 5/2
        ```
        """

        v = cls("")
        name = str(id(v))
        if ending:
            name += ending
        v.name = name
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