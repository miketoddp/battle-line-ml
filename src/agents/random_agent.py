"""
Baseline Battle Line player that selects legal moves at random.

Based on a GameState object, calls `legal_move(state)`.

Returns one random move.
"""

from game.state import GameState
from game.move import Move
from game.rules import legal_moves
import random

class RandomAgent:
    def choose_move(self, state: GameState) -> Move:
        moves = legal_moves(state)
        return random.choice(moves)