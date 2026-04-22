"""
Rules representation for Battle Line.

Logic: defines what is legal and how outcomes are computed.

Legal moves, formation rank, checks flag winner, determines terminal state.

Called by `engine.py`. 
"""

from game.cards import Card
from game.move import Move
from game.state import GameState
from copy import deepcopy

def legal_moves(state: GameState) -> list[Move]:
    ... 

def 