"""
Battle Line player that selects legal moves based on defined strategy.

Based on a GameState object, calls `legal_moves(state)`.
Then evaluates using a scoring rubric.

Returns one heuristically selected move.
"""

from game.state import GameState
from game.move import Move
from game.rules import legal_moves, formation_rank
import random

class HeuristicAgent:
    def choose_move(self, state: GameState) -> Move:
        moves = legal_moves(state)

        if not moves:
            raise ValueError("No legal moves available.")
        
        scored_moves = []

        for move in moves:
            score = self.score_move(state, move)
            scored_moves.append((score, move))

        best_score = max(score for score, move in scored_moves)
        best_moves = [move for score, move in scored_moves if score == best_score]

        return random.choice(best_moves)
    
    def score_move(self, state: GameState, move: Move) -> int:
        score = 0
        opp_id = 3 - move.player_id
        own_formation = state.flags[move.target_flag][move.player_id]
        opp_formation = state.flags[move.target_flag][opp_id]

        card = state.hands[move.player_id][move.card_index]
        score += card.value // 2

        # reward completion of own strong formations
        if len(own_formation) == 2:
            score += 1

            candidate_formation = own_formation + [card]
            rank, _ = formation_rank(candidate_formation)

            if rank == 5:
                score += 6
            elif rank == 4:
                score += 5
        
        # penalize plays against strong full opponent formations
        if len(opp_formation) == 3:
            rank, _ = formation_rank(opp_formation)

            if rank == 5:
                score -= 4
            elif rank == 4:
                score -= 3

        # penalize plays against strong opponent two-card threats
        if len(opp_formation) == 2:
            opp_values = sorted([opp_formation[0].value, opp_formation[1].value])

            if opp_formation[0].value == opp_formation[1].value:
                score -= 2

            if opp_formation[0].color == opp_formation[1].color:
                if opp_values[1] - opp_values[0] <= 2:
                    score -= 3
                else: 
                    score -= 1

        return score







