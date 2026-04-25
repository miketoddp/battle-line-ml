"""
Move representation for Battle Line.

Intended to be explicit and simple.

Uses `card_id` rather than index.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    player_id: int
    card_index: int
    target_flag: int