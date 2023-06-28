from __future__ import annotations

import enum

class OptimizationValues(enum.Enum):
    INFEASIBLE = -1
    OPTIMAL = 0
    UNBOUNDED = 1