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
from agents.mcts_agent import MCTSAgent

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

def run_tournament(agent1, agent2, n_games: int = 100):
    results = {1: 0, 2: 0, None: 0}

    for _ in range(n_games):
        winner = play_game(agent1,agent2)
        results[winner] += 1
    
    return results

def main():
    n_games = 50

    print("MCTS vs Random")
    print(run_tournament(MCTSAgent(simcount=100), RandomAgent(), n_games))

    print("Random vs MCTS")
    print(run_tournament(RandomAgent(), MCTSAgent(simcount=100), n_games))

    print("MCTS vs Heuristic")
    print(run_tournament(MCTSAgent(simcount=100), HeuristicAgent(), n_games))

    print("Heuristic vs MCTS")
    print(run_tournament(HeuristicAgent(), MCTSAgent(simcount=100), n_games))

if __name__ == "__main__":
    main()          


