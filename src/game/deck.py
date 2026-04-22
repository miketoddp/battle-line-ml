"""
Deck generation for BAttle Line.

Specifies valid cards, deck to draw from, and initial hands.
Also contains card draw function that returns `None` if deck empty.

Called by `rules.py`.

"""

import random
from game.cards import Card

# specify valid cards
COLORS: list[str] = ["red", "blue", "green", "yellow", "purple", "orange"]
VALUES: list[int] = list(range(1,11))

# create full deck via list comprehension
def create_deck() -> list[Card]:
    return [Card(color,value) for color in COLORS for value in VALUES]

# shuffle created deck in place
def shuffle_deck(deck: list[Card]) -> None: # no return value, mutates deck directly
    random.shuffle(deck)

# deal two hands of cards
def deal_hands(deck: list[Card], hand_size: int = 7) -> dict[int, list[Card]]: # key = player int, value = list of cards
    hands: dict[int, list[Card]] = {1: [], 2: []} # constructing player keys with empty list of cards in hand

    for _ in range(hand_size):
        for player in [1, 2]:
            hands[player].append(deck.pop())
    
    return hands

# drawing function
def draw_card(deck: list[Card]) -> Card | None: # returns a card or `None`
    if deck:
        return deck.pop()
    return None
