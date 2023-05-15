import nullaryFormula

class Constraint(nullaryFormula.NullaryFormula):
    '''
    Abstract Constraint class, representing a Constraint in PCMLC.

    Attributes
    ----------
    children: None
        The children of the current node. Since a cosntraint doesn't have any,
        it's None.
    _symbol: None
        The symbol used to represent the constraint syntaxically. Since it's doesn't
        have any, it's None.
    '''
    
    _symbol = None
    