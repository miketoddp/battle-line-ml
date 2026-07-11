"""
Bridge functions to create Spark-readable exports from SQLite dbs.

Opens SQLite, runs queries, writes CSV files, and closes SQLite
"""

def run_query(connection, sql: str) -> tuple[list[str], list[tuple]]:
    cursor = connection.cursor()
    cursor.execute(sql)

    headers = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    return headers, rows

def write_csv(
        output_file: str,
        headers: list,
        rows: list
        ) -> None:
    import csv

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

if __name__ == "__main__":
    from db.sqlite_manager import get_connection
    import os

    connection = get_connection()
    os.makedirs("data/exports", exist_ok=True)
          
    # query and write games, one row each
    games = run_query(
        connection,
        """
        SELECT *
        FROM games
        WHERE total_turns IS NOT NULL;
        """
        )
    write_csv(
        "data/exports/games.csv",
        games[0],
        games[1]
    )
    print(f"Wrote games.csv: {len(games[1])} rows")

    # query and write moves, one row each
    moves = run_query(
        connection,
        """
        SELECT m.*
        FROM moves m
        JOIN games g ON m.game_id = g.game_id
        WHERE g.total_turns IS NOT NULL;
        """
        )
    write_csv(
        "data/exports/moves.csv",
        moves[0],
        moves[1]
    )
    print(f"Wrote moves.csv: {len(moves[1])} rows")

    # query joined games and moves dataset
    # includes new columns for "acting agent" and whether they won
    move_outcomes = run_query(
        connection,
        """
        SELECT
            m.game_id,
            m.turn_number,
            m.player_id,
            CASE
                WHEN m.player_id = 1 THEN g.agent1
                WHEN m.player_id = 2 THEN g.agent2
            END AS acting_agent,
            m.card_index,
            m.target_flag,
            m.card_color,
            m.card_value,
            g.agent1,
            g.agent2,
            g.winner,
            CASE
                WHEN g.winner = m.player_id THEN 1
                ELSE 0
            END AS acting_player_won,
            g.total_turns
        FROM moves m
        JOIN games g ON m.game_id = g.game_id
        WHERE g.total_turns IS NOT NULL;
        """
    )
    write_csv(
        "data/exports/move_outcomes.csv",
        move_outcomes[0],
        move_outcomes[1]
    )
    print(f"Wrote move_outcomes.csv: {len(move_outcomes[1])} rows")

    print("Output files written successfully.")
    
    connection.close()


        

        




