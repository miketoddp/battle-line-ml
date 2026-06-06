"""
Tournament simulation script. 

Runs 100 tests to evaluate performance of agents.

Runs tests with competing agents playing first and second.
"""

# taken from `main.py`
from game.engine import initialize_game, apply_move
from game.rules import legal_moves, formation_rank
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent

def play_game(agent1, agent2) -> int | None:
    state = initialize_game()

    while not state.terminal:
        moves = legal_moves(state)

        if not moves:
            return None # no debug message, unlike `main`

        agent = agent1 if state.current_player == 1 else agent2
        move = agent.choose_move(state)
        state = apply_move(state, move)

    return state.winner

def run_tournament(n_games: int = 100):
    results = {1: 0, 2: 0, None: 0}

    for _ in range(n_games):
        winner = play_game(
            agent1 = RandomAgent(),
            agent2 = HeuristicAgent()
        )
        results[winner] += 1
    
    print(results)

if __name__ == "__main__":
    run_tournament(100)

