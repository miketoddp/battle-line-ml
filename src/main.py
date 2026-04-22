"""
Main script for Battle Line game.

Calls other functions and performs tests
"""

from game.deck import create_deck, shuffle_deck, deal_hands

def main():
    deck = create_deck()
    shuffle_deck(deck)
    hands = deal_hands(deck)

    print("Player 1 hand: ", hands[1])
    print("Player 2 hand: ", hands[2])
    print("Remaining deck size: ", len(deck))

if __name__ == "__main__":
    main()