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
            if(obj.getName() not in __class__.instance):
                __class__.instance[obj.getName()] = (obj.__class__, obj)
            else:
                if(not isinstance(obj,  __class__.instance[obj.getName()][0])):
                    raise Exception(f"{obj.getName()} is already define with another type.")
        else:
            raise Exception(f"{obj} is not a Variable.")
    
    @staticmethod
    def get(name):
        if(name in __class__.instance):
            return __class__.instance[name][1]
        else: raise Exception(f"{name} is not declared.")