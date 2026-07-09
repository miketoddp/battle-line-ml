"""
Reusable helpers for querying logged Battle Line simulation outcomes.
"""

import sqlite3

def agent_win_rates(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            agent1,
            agent2,
            winning_agent,
            COUNT(*) AS games
        FROM game_summary
        GROUP BY agent1, agent2, winning_agent
        ORDER BY agent1, agent2, games DESC
        """
    )

    return cursor.fetchall()

# helper validating that turn counts in `moves` and `games` match
def check_turn_counts(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            g.game_id,
            g.total_turns,
            COUNT(m.move_id) AS recorded_moves
        FROM games g
        JOIN moves m ON g.game_id = m.game_id
        GROUP BY g.game_id
        HAVING g.total_turns != COUNT(m.move_id)
        """
    )

    return cursor.fetchall()

# helper validating that no claimed target flags are invalid
def check_target_flags(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM moves
        WHERE target_flag < 1 OR target_flag > 9
        """
    ) 

    return cursor.fetchall()

if __name__ == "__main__":
    from db.sqlite_manager import get_connection

    connection = get_connection()

    print("Agent win rates: ")
    for row in agent_win_rates(connection):
        print(row)
    
    print("\nTurn mismatches: ")
    print(check_turn_counts(connection))

    print("\nInvalid target flags: ")
    print(check_target_flags(connection))

    connection.close()
