"""
Game state representation for Battle Line.

Reflects current player, player's hand, ...
cards played at each flag by each player, ...
remaining deck, claimed flags, turn number, winner.
"""

from dataclasses import dataclass
from game.cards import Card

@dataclass
class GameState:
    current_player: int
    hands: dict[int, list[Card]]
    flags: dict[int, dict[int, list[Card]]] # which flag, which player, which cards
    claimed_flags: dict[int, int | None]    # which flag, flag winner either exists or doesn't
    deck: list[Card]
    turn_number: int
    terminal: bool = False
    winner: int | None = None   # game winner either exists or doesn't, default None