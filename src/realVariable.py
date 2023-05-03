import variable
import variableManager

class RealVariable(variable.Variable):
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
        variableManager.VariableManager.add(new)
        return new
