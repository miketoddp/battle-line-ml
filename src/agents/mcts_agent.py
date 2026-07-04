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
- return the most-visited child node's move
"""

import random  
from game.engine import apply_move
from game.move import Move
from game.state import GameState
from game.rules import legal_moves
from mcts.node import Node
from mcts.determinization import determinize_state
from agents.random_agent import RandomAgent
from math import log, sqrt


class MCTSAgent:
    def __init__(self, simcount: int = 10, 
                 num_determinizations: int = 5):
        self.simcount = simcount
        self.num_determinizations = num_determinizations
    
    def choose_move(self, state: GameState) -> Move:
        root_player = state.current_player
        # root_node = Node(state) # removed after determinization included
        move_stats: dict[Move, dict[str, float]] = {} # float used in case of draws, later

        for _ in range(self.num_determinizations):
            fresh_state = determinize_state(state, root_player)
            fresh_root = Node(fresh_state)

            for _ in range(self.simcount):
                node = self.select_node(fresh_root)

                if node.untried_moves:
                    node = self.expand_node(node)

                # simulate from selected/expanded node...
                # ...and score result from root player's perspective
                final_state = self.rollout(node.state)
                reward = 1 if final_state.winner == root_player else 0
                self.backpropagate(node, reward)

            # within mini-tree, choose the root child explored most often
            # ...(equivalent to for-loop comparison)
            if not fresh_root.children:
                continue

            best_child = max(fresh_root.children, key=lambda child: child.visits)

            if best_child.move is None:
                raise ValueError("Best child has no move.") # implementation check
            
            assert best_child.move in legal_moves(state)
            self.record_move_stats(move_stats=move_stats, move=best_child.move, 
                                   visits=best_child.visits, wins=best_child.wins)

        if not move_stats:
            raise ValueError("Move stats were not created.")
        
        best_move = max(move_stats, key=lambda move: move_stats[move]["wins"] /
                        move_stats[move]["visits"])
        
        return best_move

    def select_node(self, node: Node) -> Node:
        # walks down the existing tree using UCB1.
        # stops at a terminal node, one with untried moves, or one with no children
        # UCB1: (child.wins / child.visits) + c * sqrt(log(node.visits) / child.visits)
        # c = sqrt(2) ~ 1.414

        while not node.state.terminal and not node.untried_moves and node.children:
            best_child = self.best_ucb_child(node)

            ## obviated with checks included in best_ucb_child
            # if best_child is None:
            #     return node
            
            node = best_child

        return node

    def best_ucb_child(self, node: Node) -> Node:
        # guard against failure if no children
        if not node.children:
            raise ValueError("Cannot select UCB child from node with no children.")
        
        # guard against failure of log(node.visits)
        if node.visits == 0:
            return random.choice(node.children)
        
        best_score = float("-inf")
        best_node = node.children[0]
        
        for child in node.children:
            # if child.visits == 0, return that child immediately
            if child.visits == 0:
                return child
            
            child_score = (
                (child.wins / child.visits)
                + sqrt(2) * sqrt(log(node.visits) / child.visits)
            )
            
            if child_score > best_score:
                best_score = child_score
                best_node = child
        
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
    
    def rollout(self, state: GameState) -> GameState:
        # plays a selected state to completion
        rollout_state = state
        agent = RandomAgent()

        while not rollout_state.terminal:
            moves = legal_moves(rollout_state)

            if not moves:
                break

            next_move = agent.choose_move(state=rollout_state)
            rollout_state = apply_move(state=rollout_state, move=next_move)

        return rollout_state

    def backpropagate(self, node: Node, reward: int = 1) -> None:
        # updates every node from the rollout node back to the root
        # move up the tree until there is no parent
        # root node gets updated too

        current_node = node

        while current_node is not None:
            current_node.visits += 1
            current_node.wins += reward # assumes root player's perspective
            current_node = current_node.parent

    def record_move_stats(self, move_stats: dict[Move, dict[str, float]], 
                          move: Move, visits: int, wins: int) -> None:
        
        if move not in move_stats:
            move_stats[move] = {"visits": 0, "wins": 0}
        
        move_stats[move]["visits"] += visits
        move_stats[move]["wins"] += wins
