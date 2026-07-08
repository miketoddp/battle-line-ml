CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent1 TEXT NOT NULL,
    agent2 TEXT NOT NULL,
    winner INTEGER,
    total_turns INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS moves (
    move_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    turn_number INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    card_index INTEGER NOT NULL,
    target_flag INTEGER NOT NULL,
    card_color TEXT NOT NULL,
    card_value INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

CREATE VIEW IF NOT EXISTS game_summary AS
SELECT
    g.game_id,
    g.agent1,
    g.agent2,
    g.winner,
    CASE
        WHEN g.winner = 1 THEN g.agent1
        WHEN g.winner = 2 THEN g.agent2
        ELSE "Draw"
    END AS winning_agent,
    g.total_turns
    g.created_at
FROM games g;