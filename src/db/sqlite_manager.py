"""
Module for connecting to and initializing SQLite database.

Database contains stored simulated games and moves of Battle line
"""

import sqlite3

def get_connection():
    con = sqlite3.connect("data/battle_line_games.sqlite")
    return con

def initialize_db():
    battle_db = get_connection()

    with open("src/db/schema.sql", "r") as file:
        schema = file.read()

    battle_db.executescript(schema)
    battle_db.commit()
    battle_db.close()

if __name__ == "__main__":
    initialize_db()