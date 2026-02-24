"""Global immutable constants for object navigation.

These values are intended to be stable across experiments. Runtime-configurable
values should live in YAML configs under configs/ or in dataclass configs.
"""

from __future__ import annotations

from typing import Final, Tuple, FrozenSet

# --- Action sets ---
ACTIONS: Final[FrozenSet[str]] = frozenset(
    {
        "move_forward",
        "turn_left",
        "turn_right",
    }
)

# --- Coordinate/frame constants ---
# Local agent forward direction in Habitat (default): -Z.
CAMERA_DEFAULT_DIRECTION: Final[Tuple[float, float, float]] = (0.0, 0.0, -1.0)
AGENT_DEFAULT_DIRECTION: Final[Tuple[float, float, float]] = (0.0, 0.0, 1.0)
CAMERA_DEFAULT_YAW_OFFSET_DEGREES: Final[float] = 180.0  # to convert from camera forward to agent forward

# --- Simulation parameters ---
CONFIDENCE_THRESHOLD: Final[float] = 0.80
LOCATION_ERROR_THRESHOLD: Final[float] = 0.5  # meters
MAX_ITER_COEF: Final[float] = 0.75  # coefficient to determine max iterations
PSEUDO_COUNT_THRESHOLD: Final[float] = 6.0

# --- Probabilistic model parameters ---
DIRICHLET_PRIOR: Final[float] = 1.0

__all__ = [
    "ACTIONS",
    "AGENT_DEFAULT_DIRECTION",
    "CAMERA_DEFAULT_DIRECTION",
    "CAMERA_DEFAULT_YAW_OFFSET_DEGREES",
    "CONFIDENCE_THRESHOLD",
    "LOCATION_ERROR_THRESHOLD",
    "MAX_ITER_COEF",
    "PSEUDO_COUNT_THRESHOLD",
    "DIRICHLET_PRIOR",
]