# Battle Line Simulation & ML Project

## Overview

This project aims to uncover effective strategies for Reiner Knizia's *Battle Line* card game (published by GMT Games, 2000) using simulation, heuristic agents, and Monte Carlo Tree Search (MCTS). 

MCTS has been used to identify strong playing approaches for two-player games such as Go as well as multi-player, non-deterministic games such as Klaus Teuber's *Catan*. *Battle Line* is a two-player, deterministic game where players win by capturing a sufficient number of flags using poker-like card formations.

This repo contains: 
- Python code for core game objects, rules, and engine logic;
- Random, heuristic, and MCTS-style agents; 
- Logged self-play simulations;
- SQLite storage for games, moves, and outcomes;
- CSV export functions for future PySpark-based analysis and feature engineering.

## Structure

- `src/game/` – core game logic, cards, moves, rules, and engine
- `src/agents/` – decision-making agents
- `src/mcts/` – MCTS implementation and determinization helpers
- `src/db/` – SQLite schema, database helpers, queries, and exports
- `src/simulation/` – tournament and self-play scripts
- `data/` – local generated data (not tracked by Git)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Run logged simulations using:**
```bash
PYTHONPATH=./src python src/simulation/tournament.py
```

**Initialize database using:**
```bash
PYTHONPATH=./src python src/db/sqlite_manager.py
```

**Exporting CSVs:**
```bash
PYTHONPATH=./src python src/db/export.py
```

*Note: SQLite database and CSV exports are ignored from Git.*

## Status and Roadmap

The project currently supports simulated games between random, heuristic, and MCTS-style agents. Logged simulations write game-level and move-level data to SQLite. 

The MCTS implementation includes parameters such as numbers of simulations and hidden information determinizations. Currently, move logs are thin and may not represent sufficient detail to uncover novel effective strategies. In particular, it does not include a full board-state feature representation at each move.

The export script for creating CSV files for later ingest is operational, but PySpark analysis has not yet been conducted. Future developments to include:
- Improved per-move feature logging;
- Development of ML-ready dataset in PySpark;
- Exploratory analysis of agent behavior and outcomes; 
- Training and evaluation of simple models for move or outcome prediction;
- In-depth analysis to improve heuristic agent strategies.