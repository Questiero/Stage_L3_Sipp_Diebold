from abc import ABC

class Variable(ABC):
    _name : str = ""

    def __init__(self):
        raise NotImplementedError("Variable can't have an instance")

    def getName(self) -> str:
        """
            Method used to get the name of a variable
            :return:
        """
        return self._name
    
    def declare(name : str):
        """
            Function used to declare a new variable.
            If this variable already exist and have another type compared to the new declaraton,
            This function will raise an Exception.

            :param name: Name of the new variable
            :returns: A variable
        """
        raise NotImplementedError("Function declare not implemented")
    
    def __str__(self):
        return self._name
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.getName() == other.getName()
        return False
    
    def __hash__(self) -> int:
        return self._name.__hash__()