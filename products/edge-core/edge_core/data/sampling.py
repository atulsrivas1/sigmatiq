"""Map logical cadence to a resample rule (skeleton).

This is a placeholder to align with sigmatix-edge-skeleton. Replace the mapping
with your concrete cadence rules as needed.
"""

from typing import Literal

Cadence = Literal["minute", "hour", "day", "week"]

def cadence_to_rule(cadence: Cadence) -> str:
    return {
        "minute": "T",
        "hour": "H",
        "day": "D",
        "week": "W",
    }.get(cadence, "H")

