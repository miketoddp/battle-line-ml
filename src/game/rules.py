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

def check_winner(state: GameState, flag: int) -> int | None:
    if len(state.flags[flag][1]) < 3 \
    or len(state.flags[flag][2]) < 3:
        return None
    
    player1_flag = formation_rank(state.flags[flag][1])
    player2_flag = formation_rank(state.flags[flag][2])

    if player1_flag[0] > player2_flag[0]:
        return 1
    elif player2_flag[0] > player1_flag[0]:
        return 2
    elif player1_flag[1] > player2_flag[1]:
        return 1
    elif player2_flag[1] > player1_flag[1]:
        return 2
    else:
        return None  
        
def is_terminal(state: GameState) -> bool:
    for player in [1,2]:
        player_flags = []

        for flag, owner in state.claimed_flags.items():
            if owner == player:
                player_flags.append(flag)

        player_flags = set(player_flags)

        if len(player_flags) >= 5:
            return True
        
        elif len(player_flags) >= 3:
            for start in range(7):
                if start in player_flags and \
                start + 1 in player_flags and \
                start + 2 in player_flags:
                    return True
        
    return False
    
