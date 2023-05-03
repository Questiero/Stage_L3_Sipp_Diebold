import variable

class VariableManager:
    instance = {}
    @staticmethod
    def add(obj):
        """
            Function used for adding an instance of a variable in the instance's dictionary
            
            :params obj: the new variable
        """
        if(isinstance(obj, variable.Variable)):
            if(obj.getName() not in __class__.instance):
                __class__.instance[obj.getName()] = (obj.__class__, obj)
            else:
                if(not isinstance(obj,  __class__.instance[obj.getName()][0])):
                    raise TypeError(f"{obj.getName()} is already define with another type.")
        else:
            raise TypeError(f"{obj} is not a Variable.")
    
    @classmethod
    def get(cls, name : str) -> variable.Variable:
        """
            Function used for getting a variable wich already exist
        
            :param name: Name of a variable
            :returns: A variable
        """
        if(name in cls.instance):
            return cls.instance[name][1]
        else: raise NameError(f"{name} is not declared.")
    
    @staticmethod
    def declare(classe, name : str):
        obj = classe.__new__(name)