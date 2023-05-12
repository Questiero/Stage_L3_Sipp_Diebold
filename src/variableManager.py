import variable
import re

class VariableManager:
    '''
    VariableManager class, used to manage all instances of Variable.
    
    Attributes
    ----------
    dict(String, Variable): instance
        A dictionnary of all instances of Variables

    '''
    
    instance = {}
    pattern = re.compile("^[a-zA-Z]([a-zA-Z0-9_])*$")

    @staticmethod
    def verifie(name : str, cls):
        '''
        Static method to verifie if a Variable can be add to the VariableManager.
    
        Attributes
        ----------
        name: String
            name of the variable

        cl: class
            Class of the variable
        
        Raises
        ------
        TypeError
            If the Variable is not a Variable, already defined with another Type or the name of the variable is not valid according to a pattern.
        '''
        if not __class__.pattern.match(name) : raise NameError(f"{name} is not a valide name for a variable")
        if name in __class__.instance and cls !=  __class__.instance[name].__class__: raise TypeError(f"{name} is already define with another type.")

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
            __class__.instance[obj.name] = obj
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