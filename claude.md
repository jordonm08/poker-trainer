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
- **Application Type**: Web-based localhost application (Flask)
- **Backend**: Python with Flask
- **Frontend**: HTML/CSS/JavaScript with visual poker table interface
- **Database**: Session-based (no database yet - stats stored in Flask sessions)
- **Poker Engine**: Custom Python implementation using standard 52-card deck

## Design Decisions
- **Table Structure**: 6-max poker (UTG, MP, CO, BTN, SB, BB)
- **Stack sizes**: Ignored for now (focus on positional play and hand strength)
- **Positions**: Analyzed and factored into grading with helper text for beginners
- **Deck**: Standard 52-card deck for all scenarios
- **Grading system**: Excellent/Good/Inaccurate/Mistake/Blunder (with best choice shown)
- **Information Flow**: Action history shown FIRST, then position/cards, then decision
- **Scenario Generation**: Unlimited scenarios with adaptive difficulty

## Current Status
- Project initialized ✓
- Repository: https://github.com/jordonm08/poker-trainer.git
- Status: **WEB VERSION COMPLETE WITH ENDLESS MODE**
- Beautiful visual web interface running on localhost
- 8 fixed practice scenarios (beginner + intermediate)
- Unlimited adaptive scenario generation
- Easy launcher scripts with shell aliases

## Development Notes
- Last updated: 2026-01-07
- This file should be updated regularly to maintain context across sessions

## What's Working (v1.0 - Web Edition)
1. ✓ Core poker logic (52-card deck, hand evaluation, 6-max positions)
2. ✓ Scenario system with action history display
3. ✓ GTO-based grading engine with explanations
4. ✓ Beautiful Flask web interface with visual poker table
5. ✓ Position helper text for beginners
6. ✓ 8 fixed practice scenarios (beginner + intermediate)
7. ✓ **NEW: Unlimited scenario generator with difficulty configs**
8. ✓ **NEW: Adaptive difficulty system (auto-adjusts based on performance)**
9. ✓ **NEW: Endless Mode with infinite randomly-generated scenarios**
10. ✓ Session-based stats tracking

## How to Run
```bash
# CLI version (original)
poker

# Web version (recommended)
poker-web

# Or manually:
cd poker-trainer
python3 -m src.web.app
# Then open http://localhost:5000
```

## Game Modes
1. **Practice Mode (Fixed Scenarios)**
   - Beginner: 6 scenarios with strong hands in good positions
   - Intermediate: 4 scenarios with marginal hands and complex decisions

2. **Endless Mode (Adaptive Difficulty)**
   - Unlimited randomly generated scenarios
   - Starts at beginner difficulty
   - Automatically promotes to intermediate/advanced based on performance
   - Tracks rolling average of last 10 decisions
   - Never runs out of hands to practice

## What's Next (Future Enhancements)
1. Post-flop scenario generation and evaluation
2. Database integration (SQLite for long-term progress tracking)
3. Visual difficulty level indicator in UI
4. Equity calculator integration
5. Hand range charts display
6. Board texture analysis for postflop
7. Multi-street scenarios (flop → turn → river)
8. Bet sizing evaluation (currently simplified)
9. Push notifications when difficulty level changes

## Project Structure (Current)
```
poker-trainer/
├── src/
│   ├── core/
│   │   ├── __init__.py      # Position enum and card parsing
│   │   ├── deck.py          # Card deck, Rank, Suit management
│   │   ├── hand_eval.py     # Hand evaluation (pairs, flushes, etc)
│   │   └── positions.py     # 6-max position definitions
│   ├── scenarios/
│   │   ├── scenario.py      # Scenario class with action history
│   │   ├── library.py       # 8 pre-built scenarios (6-max)
│   │   ├── generator.py     # NEW: Random scenario generation
│   │   └── adaptive.py      # NEW: Adaptive difficulty tracking
│   ├── grading/
│   │   ├── evaluator.py     # Decision grading (5-star system)
│   │   └── theory.py        # GTO opening ranges, pot odds
│   ├── ui/
│   │   └── app.py           # CLI interface (original)
│   └── web/
│       ├── app.py           # Flask backend with API endpoints
│       ├── templates/
│       │   └── index.html   # Main page with Endless Mode
│       └── static/
│           ├── style.css    # Green poker table styling
│           └── app.js       # Frontend logic with adaptive mode
├── tests/
├── play.sh                  # CLI launcher (alias: poker)
├── web.sh                   # Web launcher (alias: poker-web)
├── requirements.txt
└── claude.md                # This file
```

## Implementation Notes
- Fixed Python Enum value conflicts by using custom attribute names (rank_value, grade_value)
- Converted from 9-max to 6-max table structure for more realistic scenarios
- Action history displays BEFORE hand cards (natural information flow)
- Position helper text added for beginner-friendliness
- GTO-based opening ranges implemented for all 6-max positions
- Grading system provides context-aware explanations
- Adaptive difficulty uses sliding window of 10 recent decisions
- Scenario generator creates weighted-random realistic poker situations
- Flask sessions manage stats (no database yet)

---

**Note to Claude**: This file contains project context. Please read this file at the start of each session to understand the current state of the project. Update this file when significant progress is made or decisions are finalized.
