from abc import ABC, abstractmethod
import domain

class DistanceFunction(ABC):
    
    _domaine : domain.Domain
    
    @abstractmethod
    def dist(x,y):
        pass