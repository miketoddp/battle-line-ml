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
import sqlite3
from db.insert import create_game, record_move, finish_game
from db.sqlite_manager import get_connection

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

def play_and_log(agent1, agent2, connection) -> int | None:
    game_id = create_game(connection,
                          agent1.__class__.__name__, 
                          agent2.__class__.__name__
                          )
    
    state = initialize_game()
    turn_number = 0

    while not state.terminal:
        moves = legal_moves(state)

        if not moves:
            # close connection if no legal moves
            finish_game(connection, game_id, winner=None, 
                        total_turns=turn_number)
            return None
        
        agent = agent1 if state.current_player == 1 else agent2
        move = agent.choose_move(state)

        # get card from state before applying move, will be overwritten
        card = state.hands[move.player_id][move.card_index]

        # then increment turn and record
        turn_number += 1
        record_move(connection, game_id, turn_number, move, card)

        state = apply_move(state, move)
    
    finish_game(connection, game_id, winner=state.winner, 
                total_turns=turn_number)
    
    return state.winner

def run_tournament(agent1, agent2, n_games: int = 100):
    results = {1: 0, 2: 0, None: 0}

    for _ in range(n_games):
        winner = play_game(agent1,agent2)
        results[winner] += 1
    
    return results

def run_logged_tournament(agent1, agent2, n_games: int = 50):
    results = {1: 0, 2: 0, None: 0}

    connection = get_connection()

    for _ in range(n_games):
        winner = play_and_log(agent1,
                              agent2,
                              connection=connection)
        results[winner] += 1

    connection.close()
    return results
    
# def main():
#     connection = get_connection()

#     winner = play_and_log(
#         agent1=RandomAgent(),
#         agent2=HeuristicAgent(),
#         connection=connection
#     )
    
#     connection.close()
#     print("Logged one game. Winner: ", winner)

def main():

    print("MCTS vs Random")
    print(run_logged_tournament(MCTSAgent(), RandomAgent(), n_games=10))

    print("Random vs MCTS")
    print(run_logged_tournament(RandomAgent(), MCTSAgent(), n_games=10))

    print("MCTS vs Heuristic")
    print(run_logged_tournament(MCTSAgent(), HeuristicAgent(), n_games=10))

    print("Heuristic vs MCTS")
    print(run_logged_tournament(HeuristicAgent(), MCTSAgent(), n_games=10))

if __name__ == "__main__":
    main()          


