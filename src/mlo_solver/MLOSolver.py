from __future__ import annotations

from abc import ABC

class MLOSolver(ABC):
    def __init__(self):
        raise NotImplementedError("Solver can't have an instance")
    def solve(self, variables : list, objectif : dict, constraints : dict) -> tuple:
        raise NotImplementedError("Method solve is not implemented")