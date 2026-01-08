"""
Basic tests to verify core functionality.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core import Card, Deck, Rank, Suit, Position, parse_card, get_hand_notation
from src.scenarios import create_simple_scenario, Action
from src.grading import DecisionEvaluator, Grade


def test_card_creation():
    """Test creating cards."""
    card = Card(Rank.ACE, Suit.SPADES)
    assert str(card) == "A♠"
    print("✓ Card creation works")


def test_deck():
    """Test deck functionality."""
    deck = Deck()
    assert len(deck) == 52

    card = deck.deal_one()
    assert isinstance(card, Card)
    assert len(deck) == 51
    print("✓ Deck works")


def test_parse_card():
    """Test card parsing."""
    card = parse_card("As")
    assert card.rank == Rank.ACE
    assert card.suit == Suit.SPADES
    print("✓ Card parsing works")


def test_hand_notation():
    """Test hand notation."""
    from src.core import parse_cards

    # Pocket aces
    cards = parse_cards("As Ad")
    notation = get_hand_notation(cards)
    assert notation == "AA"

    # AK suited
    cards = parse_cards("As Ks")
    notation = get_hand_notation(cards)
    assert notation == "AKs"

    # AK offsuit
    cards = parse_cards("As Kh")
    notation = get_hand_notation(cards)
    assert notation == "AKo"

    print("✓ Hand notation works")


def test_scenario_creation():
    """Test creating a scenario."""
    scenario = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Ah",
        pot_size=1.5,
        current_bet=0.0,
    )

    assert scenario.hero_position == Position.BTN
    assert len(scenario.hero_cards) == 2
    assert scenario.pot_size == 1.5
    print("✓ Scenario creation works")


def test_decision_evaluation():
    """Test decision evaluation."""
    scenario = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Ah",
        pot_size=1.5,
        current_bet=0.0,
    )

    evaluator = DecisionEvaluator()

    # Test correct decision (raise with AA)
    evaluation = evaluator.evaluate_decision(scenario, Action.RAISE)
    assert evaluation.grade == Grade.EXCELLENT
    print("✓ Decision evaluation works (correct)")

    # Test incorrect decision (fold AA)
    evaluation = evaluator.evaluate_decision(scenario, Action.FOLD)
    assert evaluation.grade in [Grade.BLUNDER, Grade.MISTAKE]
    print("✓ Decision evaluation works (incorrect)")


def test_weak_hand_fold():
    """Test that weak hands should fold."""
    scenario = create_simple_scenario(
        hero_position=Position.UTG,
        hero_cards_str="7h 2d",
        pot_size=1.5,
        current_bet=0.0,
    )

    evaluator = DecisionEvaluator()
    evaluation = evaluator.evaluate_decision(scenario, Action.FOLD)
    assert evaluation.grade == Grade.EXCELLENT
    print("✓ Weak hand evaluation works")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Running basic tests...")
    print("="*60 + "\n")

    test_card_creation()
    test_deck()
    test_parse_card()
    test_hand_notation()
    test_scenario_creation()
    test_decision_evaluation()
    test_weak_hand_fold()

    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
