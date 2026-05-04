"""
Main script for Battle Line game.

Calls other functions and performs tests
"""

from game.deck import create_deck, shuffle_deck, deal_hands
from game.engine import initialize_game, apply_move
from game.rules import legal_moves, formation_rank
import random

def main():
# tests for deck creation (pre-initialize)
    # deck = create_deck()
    # shuffle_deck(deck)
    # hands = deal_hands(deck)

    # print("Player 1 hand: ", hands[1])
    # print("Player 2 hand: ", hands[2])
    # print("Remaining deck size: ", len(deck))

    state = initialize_game()
    last_move = None

    while not state.terminal:
        moves = legal_moves(state)

        if not moves:
            print("No legal moves available.")
            break 

        move = random.choice(moves)
        last_move = move

        print(f"Player {state.current_player} plays {move}")
        state = apply_move(state, move)

    print("Claimed flags: ", state.claimed_flags)
    print("Game over. Winner: ", state.winner)
    winner_flags = [
        f for f, owner in state.claimed_flags.items()
        if owner == state.winner
    ]
    
    print("Winner claimed final flag(s): ", winner_flags)

    if last_move is not None:
        flag = last_move.target_flag
        print("Final flag: ", flag)
        print("Player 1 final flag cards: ", state.flags[flag][1])
        print("Player 1 final flag rank: ", formation_rank(state.flags[flag][1]))
        print("Player 2 final flag cards: ", state.flags[flag][2])
        print("Player 2 final flag rank: ", formation_rank(state.flags[flag][2]))

# tests for hand composition
    # print("Current player:", state.current_player)
    # print("Player 1 hand size: ", len(state.hands[1]))
    # print("Player 2 hand size: ", len(state.hands[2]))
    # print("Remaining deck size: ", len(state.deck))
    # print("Number of flags: ", len(state.flags))
    # print("Claimed flags: ", state.claimed_flags)

if __name__ == "__main__":
    main()