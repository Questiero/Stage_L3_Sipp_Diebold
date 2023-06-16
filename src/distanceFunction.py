from abc import ABC, abstractmethod
from .domain import Domain

class DistanceFunction(ABC):
    
    _domaine : Domain
    
    @abstractmethod
    def dist(x,y):
        pass