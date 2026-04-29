"""
State transitions for Battle Line games.

Returns new or mutated GameState object.

Creates initial game states and applies moves to produce updated GameState
objects. Handles move execution, flag-claim updates, and turn advancement.

Calls `rules.py`, but `rules.py` should not depend on `engine.py`.
"""

from game.move import Move
from game.state import GameState
import game.deck as deck
import game.rules as rules
from copy import deepcopy

def initialize_game(seed: int | None = None) -> GameState:
    # Create deck, shuffle, deal, create flags, ...
    # ... create empty claimed flags, return GameState.
    # Uses `deck.py`.
    
    this_deck = deck.create_deck()
    deck.shuffle_deck(this_deck)
    these_hands = deck.deal_hands(this_deck)

    flags = {i: {1: [], 2: []} for i in range(1,10)}
    claimed_flags: dict[int, int | None] \
        = {i: None for i in range(1,10)}

    this_game = GameState(
        current_player=1,
        hands=these_hands,
        flags=flags,
        claimed_flags=claimed_flags,
        deck=this_deck,
        turn_number=0,
        terminal=False,
        winner=None,
    )

    return this_game

def update_claims(state: GameState) -> GameState:
    # Loop thru flags, skipping claimed ones...
    # ... check for winner, changing as necessary.
    ...

def apply_move(state: GameState, move: Move) -> GameState:
    # Copy state, remove selected card, place on target flag...
    # ... draw replacement from deck (if not empty), update claims...
    # ... check terminal state, advance turn if not terminal...
    # ... return new state. 
    # Uses `deepcopy`.
    
    new_state = deepcopy(state)

    hand = new_state.hands[move.player_id]
    card = hand.pop(move.card_index)

    new_state.flags[move.target_flag][move.player_id].append(card)

    if new_state.deck:
        draw = new_state.deck.pop()
        new_state.hands[move.player_id].append(draw)
    
    new_state = update_claims(new_state)

    if rules.is_terminal(new_state) == True:
        new_state.terminal = True
    else: 
        new_state = advance_turn(new_state)

    return new_state

def advance_turn(state: GameState) -> GameState:
    state.current_player = 3 - state.current_player
    # If player 1, return 2; if player 2, return 1.
    state.turn_number += 1
    return state
