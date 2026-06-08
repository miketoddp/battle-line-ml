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