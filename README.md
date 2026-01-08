# Poker Trainer

Train your poker skills through scenario-based decision making, similar to chess.com's tactical trainers. Available as both a web app and command-line interface.

## Setup

```bash
pip install -r requirements.txt
```

## Run

### Web Version (Recommended)
Beautiful visual interface with poker table graphics:
```bash
./web.sh
```
Then open http://localhost:5000 in your browser.

Or use the shortcut (after `source ~/.zshrc`):
```bash
poker-web
```

### Command-Line Version
Simple text-based interface:
```bash
python -m src.ui.app
```

Or use the shortcut:
```bash
poker
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
