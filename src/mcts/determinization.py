"""
Helper function to establish possible future game states conditioned on hidden info.

Accepts input state and POV player id, then returns modified GameState.

Called by MCTSAgent, which uses determinized state to conduct rollout.

"""

from game.state import GameState
from game.deck import shuffle_deck
from copy import deepcopy

def determinize_state(state: GameState, player_id: int) -> GameState:
    possible_state = deepcopy(state)
    opp_id = 3 - player_id
    opp_hand_len = len(possible_state.hands[opp_id])

    # create unknown pool from copied deck and unknown opponent hand
    unknown_pool = possible_state.deck + possible_state.hands[opp_id]
    shuffle_deck(unknown_pool)

    # clear opponent's copied hand
    possible_state.hands[opp_id] = []

    # redeal possible opponent hand
    for _ in range(opp_hand_len):
        possible_state.hands[opp_id].append(unknown_pool.pop())

    possible_state.deck = unknown_pool

    return possible_state
