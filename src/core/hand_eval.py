"""
Poker hand evaluation and ranking.
"""
from enum import Enum
from typing import List, Tuple
from collections import Counter
from .deck import Card, Rank


class HandRank(Enum):
    """Poker hand rankings from highest to lowest."""
    ROYAL_FLUSH = (10, "Royal Flush")
    STRAIGHT_FLUSH = (9, "Straight Flush")
    FOUR_OF_A_KIND = (8, "Four of a Kind")
    FULL_HOUSE = (7, "Full House")
    FLUSH = (6, "Flush")
    STRAIGHT = (5, "Straight")
    THREE_OF_A_KIND = (4, "Three of a Kind")
    TWO_PAIR = (3, "Two Pair")
    ONE_PAIR = (2, "One Pair")
    HIGH_CARD = (1, "High Card")

    def __init__(self, rank_value: int, description: str):
        self.rank_value = rank_value
        self.description = description

    def __lt__(self, other):
        return self.rank_value < other.rank_value

    def __str__(self):
        return self.description


class HandStrength:
    """Represents the strength of a poker hand for comparison."""

    def __init__(self, rank: HandRank, tiebreakers: List[int]):
        """
        Args:
            rank: The hand ranking (pair, flush, etc.)
            tiebreakers: List of card values for breaking ties, in order of importance
        """
        self.rank = rank
        self.tiebreakers = tiebreakers

    def __lt__(self, other: 'HandStrength') -> bool:
        """Compare hand strengths."""
        if self.rank.rank_value != other.rank.rank_value:
            return self.rank.rank_value < other.rank.rank_value

        # Same rank, compare tiebreakers
        for my_val, other_val in zip(self.tiebreakers, other.tiebreakers):
            if my_val != other_val:
                return my_val < other_val

        return False  # Hands are equal

    def __eq__(self, other: 'HandStrength') -> bool:
        """Check if hands are equal."""
        return (self.rank == other.rank and
                self.tiebreakers == other.tiebreakers)

    def __str__(self) -> str:
        return str(self.rank)


def evaluate_hand(cards: List[Card]) -> HandStrength:
    """
    Evaluate a 5-7 card poker hand.

    Args:
        cards: List of 5-7 cards (hole cards + board)

    Returns:
        HandStrength object

    Raises:
        ValueError: If not 5-7 cards provided
    """
    if not 5 <= len(cards) <= 7:
        raise ValueError(f"Must evaluate 5-7 cards, got {len(cards)}")

    # For 7 cards, we'd need to check all combinations
    # For now, simplified to best 5-card evaluation
    if len(cards) == 7:
        # Find best 5-card hand from 7 cards
        from itertools import combinations
        best = None
        for combo in combinations(cards, 5):
            strength = _evaluate_five_cards(list(combo))
            if best is None or strength > best:
                best = strength
        return best
    elif len(cards) == 6:
        from itertools import combinations
        best = None
        for combo in combinations(cards, 5):
            strength = _evaluate_five_cards(list(combo))
            if best is None or strength > best:
                best = strength
        return best
    else:
        return _evaluate_five_cards(cards)


def _evaluate_five_cards(cards: List[Card]) -> HandStrength:
    """Evaluate exactly 5 cards."""
    assert len(cards) == 5

    ranks = sorted([c.rank.rank_value for c in cards], reverse=True)
    suits = [c.suit for c in cards]
    rank_counts = Counter([c.rank.rank_value for c in cards])

    is_flush = len(set(suits)) == 1
    is_straight = _check_straight(ranks)

    # Check for royal flush
    if is_flush and is_straight and ranks[0] == 14:
        return HandStrength(HandRank.ROYAL_FLUSH, ranks)

    # Check for straight flush
    if is_flush and is_straight:
        return HandStrength(HandRank.STRAIGHT_FLUSH, ranks)

    # Check for four of a kind
    if 4 in rank_counts.values():
        quad = [r for r, count in rank_counts.items() if count == 4][0]
        kicker = [r for r, count in rank_counts.items() if count == 1][0]
        return HandStrength(HandRank.FOUR_OF_A_KIND, [quad, kicker])

    # Check for full house
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        trips = [r for r, count in rank_counts.items() if count == 3][0]
        pair = [r for r, count in rank_counts.items() if count == 2][0]
        return HandStrength(HandRank.FULL_HOUSE, [trips, pair])

    # Check for flush
    if is_flush:
        return HandStrength(HandRank.FLUSH, ranks)

    # Check for straight
    if is_straight:
        return HandStrength(HandRank.STRAIGHT, ranks)

    # Check for three of a kind
    if 3 in rank_counts.values():
        trips = [r for r, count in rank_counts.items() if count == 3][0]
        kickers = sorted([r for r, count in rank_counts.items() if count == 1], reverse=True)
        return HandStrength(HandRank.THREE_OF_A_KIND, [trips] + kickers)

    # Check for two pair
    pairs = sorted([r for r, count in rank_counts.items() if count == 2], reverse=True)
    if len(pairs) == 2:
        kicker = [r for r, count in rank_counts.items() if count == 1][0]
        return HandStrength(HandRank.TWO_PAIR, pairs + [kicker])

    # Check for one pair
    if len(pairs) == 1:
        kickers = sorted([r for r, count in rank_counts.items() if count == 1], reverse=True)
        return HandStrength(HandRank.ONE_PAIR, pairs + kickers)

    # High card
    return HandStrength(HandRank.HIGH_CARD, ranks)


def _check_straight(ranks: List[int]) -> bool:
    """Check if ranks form a straight."""
    sorted_ranks = sorted(set(ranks), reverse=True)

    if len(sorted_ranks) < 5:
        return False

    # Check for regular straight
    if sorted_ranks[0] - sorted_ranks[4] == 4:
        return True

    # Check for wheel (A-2-3-4-5)
    if sorted_ranks == [14, 5, 4, 3, 2]:
        return True

    return False


def get_hand_category(hole_cards: List[Card]) -> str:
    """
    Categorize a starting hand (2 hole cards).

    Args:
        hole_cards: Exactly 2 cards

    Returns:
        String category: "pocket_pair", "suited", "offsuit"

    Raises:
        ValueError: If not exactly 2 cards
    """
    if len(hole_cards) != 2:
        raise ValueError("Must provide exactly 2 hole cards")

    card1, card2 = hole_cards

    if card1.rank == card2.rank:
        return "pocket_pair"
    elif card1.suit == card2.suit:
        return "suited"
    else:
        return "offsuit"


def get_hand_notation(hole_cards: List[Card]) -> str:
    """
    Get standard poker notation for starting hand.

    Args:
        hole_cards: Exactly 2 cards

    Returns:
        String notation (e.g., "AKs", "QQ", "72o")
    """
    if len(hole_cards) != 2:
        raise ValueError("Must provide exactly 2 hole cards")

    card1, card2 = hole_cards

    # Sort by rank (higher first)
    if card1.rank.rank_value < card2.rank.rank_value:
        card1, card2 = card2, card1

    notation = f"{card1.rank.symbol}{card2.rank.symbol}"

    if card1.rank == card2.rank:
        return notation  # Pocket pair, no suffix
    elif card1.suit == card2.suit:
        return notation + "s"  # Suited
    else:
        return notation + "o"  # Offsuit
