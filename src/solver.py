from abc import ABC

class Solver(ABC):
    def __init__(self):
        raise NotImplementedError("Solver can't have an instance")
    def solve(constraints : dict) -> tuple:
        raise NotImplementedError("Method solve is not implemented")