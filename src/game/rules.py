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

def formation_rank(cards: list[Card]) -> tuple:
    values = []
    colors = []

    if len(cards) != 3:
        raise ValueError(f"Expected 3 cards, got {len(cards)}")

    for card in cards:
        values.append(card.value)
        colors.append(card.color)

    values.sort()
    
    low_card = values[0]
    is_straight = values[1] == low_card + 1 and values[2] == low_card + 2
    same_color = len(set(colors)) == 1

    tie_break = values[2]

    if is_straight and same_color:
        rank = 5 # wedge formation
    elif len(set(values)) == 1:
        rank = 4 # phalanx (one value)
    elif same_color:
        rank = 3 # battalion (one color)
        tie_break = sum(values)
    elif is_straight:
        rank = 2 # skirmish (straight values)
    else:
        rank = 1 # host
        tie_break = sum(values)

    return (rank, tie_break)
    
        
        

        
    
