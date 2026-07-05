"""
Stores MCTS bookkeeping information for Battle Line rollouts. 

Initially imagined with perfect information (deck, opponent hands, etc.).

Determinization function added to establish more realistic hidden information.
"""

from game.state import GameState
from game.move import Move
from game.rules import legal_moves

class Node:
    def __init__(self, 
                 state: GameState, 
                 parent: "Node | None" = None, # forward reference
                 move: Move | None = None
    ):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: list["Node"] = []
        self.untried_moves = [] if state.terminal \
            else legal_moves(state)
        self.visits = 0
        self.wins = 0