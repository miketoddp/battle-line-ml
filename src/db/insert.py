"""
Helper function to write rows for Battle Line games and moves.
"""

import sqlite3
from game.move import Move
from game.cards import Card

def create_game(connection, agent1: str, agent2: str) -> int:
    # insert row into `games` with agent1 and agent2
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO games (agent1, agent2) 
        VALUES (?, ?)
        """,
        (agent1, agent2)
    )
    connection.commit()

    # return new game_id
    game_id = cursor.lastrowid
    return game_id

def record_move(connection, game_id: int, turn_number: int,
                move: Move, card: Card) -> None:

    player_id = move.player_id
    card_index = move.card_index
    target_flag = move.target_flag
    card_color = card.color
    card_value = card.value
    
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO moves (game_id, turn_number, player_id, card_index,
        target_flag, card_color, card_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (game_id, turn_number, player_id, card_index, target_flag,
         card_color, card_value)
    )
    connection.commit()

def finish_game(connection, game_id: int, winner: int | None,
                total_turns: int) -> None:
    
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE games
        SET winner = ?, total_turns = ?
        WHERE game_id = ?
        """,
        (winner, total_turns, game_id)
    )
    connection.commit()

if __name__ == "__main__":
    from db.sqlite_manager import get_connection
    from game.move import Move
    from game.cards import Card

    con = get_connection()

    game_id = create_game(con, "TestAgent1", "TestAgent2")

    move = Move(player_id=1, card_index=3, target_flag=5)
    card = Card(color="red", value=7)

    record_move(con, game_id, turn_number=0, move=move, card=card)

    finish_game(con, game_id, winner=1, total_turns=1)

    con.close()


