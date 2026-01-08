# Quick Start Guide

## Running the Poker Trainer

1. Navigate to the project directory:
```bash
cd poker-trainer
```

2. Run the application:
```bash
python3 -m src.ui.app
```

3. Choose from the menu:
   - **1. Practice (Beginner)** - 5 beginner scenarios
   - **2. Practice (Intermediate)** - 3 intermediate scenarios
   - **3. View Stats** - See your accuracy
   - **4. Quit** - Exit the app

## Example Scenario

```
SCENARIO 1/5: Premium Pocket Aces
============================================================

Position: Button
Your hand: A♠ A♥
Pot: 1.5BB

What do you do?
1. Fold
2. Check
3. Bet

Your choice (number): 3

EVALUATION
============================================================

Your move: BET
Grade: Excellent ★★★★★

Excellent! AA is a premium hand and should be raised from BTN.
```

## Understanding Grades

- **Excellent** ★★★★★ - Best move
- **Good** ★★★★☆ - Solid play
- **Inaccurate** ★★★☆☆ - Playable but not optimal
- **Mistake** ★★☆☆☆ - Clear error
- **Blunder** ★☆☆☆☆ - Serious mistake

## Running Tests

```bash
python3 tests/test_basic.py
```

All tests should pass with ✓ marks.

## Tips

- Pay attention to your position (earlier = tighter range)
- Premium hands (AA, KK, QQ, AK) should almost always be raised
- Weak hands (72o, 83o, etc.) should be folded from early position
- Position matters! You can play more hands from BTN than UTG

## Next Steps

See [claude.md](claude.md) for project details and future enhancements.
