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
    moves = []
    player = state.current_player
    hand = state.hands[player]

    for card_index, card in enumerate(hand):
        for flag in state.flags:
            if state.claimed_flags[flag] is None:
                if len(state.flags[flag][player]) < 3:
                    legal_move = Move(
                        player_id=player,
                        card_index = card_index,
                        target_flag=flag
                        )
                    moves.append(legal_move)
    return moves
