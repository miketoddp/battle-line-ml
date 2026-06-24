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

import random  
from game.engine import apply_move
from game.move import Move
from game.state import GameState
from mcts.node import Node
from math import log, sqrt


class MCTSAgent:
    def __init__(self, simcount: int = 100):
        self.simcount = simcount
    
    def choose_move(self, state: GameState) -> Move:
        root_player = state.current_player
        root_node = Node(state)

        for _ in range(self.simcount):
            node = self.select_node(root_node)

            if node.untried_moves:
                node = self.expand_node(node)

            final_state = self.rollout(node.state)
            reward = 1 if final_state.winner == root_player else 0

            # choose the root child explored most often and return its move
            self.backpropagate(node, reward)

        if not root_node.children:
            raise ValueError("MCTS found no child node.")
        
        best_child = max(root_node.children, key=lambda child: child.visits)
        # lambda function equivalent to for-loop comparison on child.visits
        
        if best_child.move is None:
            raise ValueError("Best child has no move.") # implementation check

        return best_child.move
            

    def select_node(self, node: Node) -> Node:
        # selects promising node -- aka, a "tree policy"
        # via UCB1 = (child.wins / child.visits) + sqrt(log(node.visits) / child.visits)
        # c = sqrt(2) ~ 1.414
        # use if child.visits == 0:
            # return float("-inf") ... so that unvisited children get tried.

        if not node.children:
            return node

        best_score = float("-inf") # unvisited children get tried
        best_node: Node | None = None

        for child in node.children:
            if child.visits == 0:
                return child
            
            child_score = (
                (child.wins / child.visits)
                + 1.414 * sqrt(log(node.visits) / child.visits)
            )
            
            if child_score > best_score:
                best_score = child_score
                best_node = child
        
        if best_node is None:
            return node
        
        return best_node

    def expand_node(self, node: Node) -> Node:
        # expands selected node if possible
        if not node.untried_moves:
            return node
    
        # select random untried move and remove it from untried_moves list        
        candidate = random.choice(node.untried_moves)
        node.untried_moves.remove(candidate)

        # apply move to node.state, create new node with resulting state
        new_node = Node(
            state=apply_move(node.state, candidate),
            parent=node,
            move=candidate
        )
        
        node.children.append(new_node)

        return new_node
    
    def rollout(self, state: GameState):
        # plays a selected state to completion
        ...
        return state

    def backpropagate(self, node: Node, reward):
        ...
