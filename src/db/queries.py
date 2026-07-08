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
