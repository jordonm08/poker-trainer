# Poker Trainer

A desktop application for training poker skills through scenario-based decision making, similar to chess.com's tactical trainers.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m src.ui.app
```

## Project Structure

- `src/core/` - Core poker logic (deck, hand evaluation, positions)
- `src/scenarios/` - Scenario management and library
- `src/grading/` - Decision grading engine
- `src/ui/` - User interface
- `src/db/` - Database operations
- `tests/` - Unit tests
- `data/` - SQLite database

## Development

See [claude.md](claude.md) for detailed project context and decisions.
