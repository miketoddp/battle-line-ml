"""
Main script for Battle Line game.

Calls other functions and performs tests
"""

from game.deck import create_deck, shuffle_deck, deal_hands
from game.engine import initialize_game

def main():
    deck = create_deck()
    shuffle_deck(deck)
    hands = deal_hands(deck)

    print("Player 1 hand: ", hands[1])
    print("Player 2 hand: ", hands[2])
    print("Remaining deck size: ", len(deck))

    state = initialize_game()

    print("Current player:", state.current_player)
    print("Player 1 hand size: ", len(state.hands[1]))
    print("Player 2 hand size: ", len(state.hands[2]))
    print("Remaining deck size: ", len(state.deck))
    print("Number of flags: ", len(state.flags))
    print("Claimed flags: ", state.claimed_flags)

if __name__ == "__main__":
    main()