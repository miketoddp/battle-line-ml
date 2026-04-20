"""
Card representations for Battle Line.

Does NOT contain game rules (card values and colors themselves).
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    color: str
    value: int