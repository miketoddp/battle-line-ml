"""
Battle Line player using Monte Carlo tree search (MCTS) to select moves.

Initially developed with perfect information.
Agent can see opponent hand and deck.

Based on a GameState object, calls `legal_moves(state)`.
Then selects next move based on simulated wins.

Specifically:
- chooses root node
- loops:
  -- select promising node
  -- expand if possible
  -- rollout to the end
  -- backpropagate result
- return best child's move
"""

from game.state import GameState
from game.move import Move
from mcts.node import Node
from math import sqrt, log


class MCTSAgent:
    def choose_move(self, state: GameState, simcount: int = 100) -> Move:
        root_player = state.current_player
        root_node = Node(state)

        for i in range(simcount):
            node = self.select_node(root_node)

            if node.untried_moves:
                node = self.expand_node(node)

            final_state = self.rollout(node.state)

            reward = 1 if final_state.winner == root_player else 0

            self.backpropagate(node, reward)
        
            # choose one child of `root_node` via UCB1 and return its `move`
        if not root_node.children:
                raise ValueError("MCTS found no child node.")
        
        best_child = max(root_node.children, key=lambda child: child.visits)
        # lambda function equivalent to for-loop comparison on child.visits
        
        if best_child.move is None:
            raise ValueError("Best child has no move.") # implementation check

        return best_child.move
            

    def select_node(self, node: Node) -> Node:
        # selects promising node
        # via UCB1 = (child.wins / child.visits) + sqrt(log(node.visits) / child.visits)
        # c = sqrt(2)
        return node

    def expand_node(self, node: Node):
        # expands selected node if possible
        return node
    
    def rollout(self, state: GameState):
        # plays a selected state to completion
        ...
        return state

    def backpropagate(self, node: Node, reward):
        ...
