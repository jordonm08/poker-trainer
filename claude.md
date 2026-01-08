# Poker Trainer - Claude Context File

## Project Overview
A poker training application similar to chess.com's tactical trainers, but for poker. The app presents players with specific poker scenarios and grades their decisions based on established poker theory (GTO - Game Theory Optimal, ICM - Independent Chip Model, etc.).

## Core Concept
- Present users with realistic poker situations
- Allow them to make decisions (fold, call, raise, bet sizing)
- Grade decisions based on poker theory and optimal play
- Provide feedback and ratings on move quality
- Track progress over time

## Poker Theory Foundation
The app will evaluate decisions based on:
- **GTO (Game Theory Optimal)**: Balanced, unexploitable play
- **Pot Odds & Equity**: Mathematical correctness of calls
- **Position**: Early, middle, late position considerations
- **Stack Depths**: Deep vs short stack strategy
- **ICM (Independent Chip Model)**: Tournament-specific considerations
- **Hand Ranges**: Appropriate ranges for different situations
- **Board Texture**: Wet vs dry boards, draw potential
- **Bet Sizing**: Standard and exploitative sizing

## Key Features (Planned)
1. Scenario-based training modules
2. Decision grading system (Excellent/Good/Inaccurate/Mistake/Blunder)
3. Explanations for correct plays
4. Progress tracking and statistics
5. Difficulty levels (beginner to advanced)
6. Different game formats (Cash game, Tournament, SNG)

## Technology Stack
- **Application Type**: Single-player desktop app (Python-based)
- **Backend**: Python
- **Frontend**: Simple UI (tkinter or similar - prioritize functionality over aesthetics)
- **Database**: SQLite (lightweight, file-based, perfect for single-player desktop app)
- **Poker Engine**: Custom Python implementation using standard 52-card deck

## Design Decisions
- **Stack sizes**: Ignored for now (focus on positional play and hand strength)
- **Positions**: Analyzed and factored into grading
- **Deck**: Standard 52-card deck for all scenarios
- **Grading system**: Excellent/Good/Inaccurate/Mistake/Blunder (with best choice shown)
- **MVP focus**: Core functionality first, polish later
- **Future**: Can evolve into web app with nicer frontend

## Current Status
- Project initialized ✓
- Repository: https://github.com/jordonm08/poker-trainer.git
- Status: **MVP COMPLETE** - Core functionality working!
- Basic CLI application ready to use
- 8 sample scenarios implemented (beginner + intermediate)
- All tests passing

## Development Notes
- Last updated: 2026-01-07
- This file should be updated regularly to maintain context across sessions

## What's Working (MVP v0.1)
1. ✓ Core poker logic (52-card deck, hand evaluation, positions)
2. ✓ Scenario system (can create and present poker situations)
3. ✓ Grading engine (evaluates decisions based on GTO theory)
4. ✓ Command-line interface (practice mode, stats tracking)
5. ✓ Preflop decision evaluation with position-based ranges
6. ✓ 8 beginner/intermediate training scenarios

## How to Run
```bash
cd poker-trainer
python3 -m src.ui.app
```

## What's Next (Future Enhancements)
1. Post-flop evaluation (currently simplified)
2. More scenarios (20-30 additional scenarios)
3. Database integration (SQLite for progress tracking)
4. Better UI (tkinter GUI or web interface)
5. Equity calculator integration
6. Hand range charts
7. Board texture analysis
8. Multi-street scenarios

## Project Structure (Planned)
```
poker-trainer/
├── src/
│   ├── core/
│   │   ├── deck.py          # Card deck management
│   │   ├── hand_eval.py     # Hand evaluation logic
│   │   └── positions.py     # Position definitions
│   ├── scenarios/
│   │   ├── scenario.py      # Scenario class and logic
│   │   └── library.py       # Pre-built scenarios
│   ├── grading/
│   │   ├── evaluator.py     # Decision grading engine
│   │   └── theory.py        # Poker theory rules
│   ├── ui/
│   │   └── app.py           # Main UI
│   └── db/
│       └── database.py      # SQLite operations
├── tests/
├── data/
│   └── scenarios.db         # SQLite database
└── requirements.txt
```

## Implementation Notes
- Fixed Python Enum value conflicts by using custom attribute names (rank_value, grade_value)
- Command-line interface provides immediate feedback on decisions
- GTO-based opening ranges implemented for all 9 positions
- Grading system provides context-aware explanations

---

**Note to Claude**: This file contains project context. Please read this file at the start of each session to understand the current state of the project. Update this file when significant progress is made or decisions are finalized.
