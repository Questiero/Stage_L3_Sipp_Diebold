from .Variable import Variable

class VariableManager:
    instance = {}
    @staticmethod
    def add(obj):
        """
            Method used for adding an instance of a Variable in the instance's dictionary
            
            params:
                obj : Variable
        """
        if(isinstance(obj, Variable)):
            if(obj._name not in __class__.instance):
                __class__.instance[obj._name] = obj.__class__
            else:
                if(not isinstance(obj,  __class__.instance[obj._name])):
                    raise Exception(f"{obj._name} is already define with another type.")
        else:
            raise Exception(f"{obj} is not a Variable.")