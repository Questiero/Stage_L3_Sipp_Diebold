import variable

class VariableManager:
    '''
    VariableManager class, used to manage all instances of Variable.
    
    Attributes
    ----------
    dict(String, Variable): instance
        A dictionnary of all instances of Variables

    '''
    
    instance = {}
    
    @staticmethod
    def add(obj: variable.Variable):
        '''
        Static method to add a Variable to the VariableManager.
    
        Attributes
        ----------
        obj: Variable
            The Variable to add
        
        Raises
        ------
        TypeError
            If the Variable is not a Variable, or already defined with another Type.
        '''
        
        if(isinstance(obj, variable.Variable)):
            if(obj.name not in __class__.instance):
                __class__.instance[obj.name] = obj
            else:
                if(not isinstance(obj,  __class__.instance[obj.name].__class__)):
                    raise TypeError(f"{obj.name} is already define with another type.")
        else:
            raise TypeError(f"{obj} is not a Variable.")
    
    @classmethod
    def get(cls, name : str) -> variable.Variable:
        '''
        Static method to get a Variable to the VariableManager.
    
        Attributes
        ----------
        obj: Variable
            The Variable to add
        
        Raises
        ------
        NameError
            The Variable isn't defined.
            
        Returns
        -------
        Variable: variable
            The defined variable.

        '''
        
        if(name in cls.instance):
            return cls.instance[name]
        else: raise NameError(f"{name} is not declared.")
    
    @staticmethod
    def declare(classe, name : str):
        '''
        Static method to declare a Variable to the VariableManager.
    
        Attributes
        ----------
        classe: Class
            The class of the Variable to declare
        name: String
            The Variable name
        '''
        
        obj = classe.__new__(name)