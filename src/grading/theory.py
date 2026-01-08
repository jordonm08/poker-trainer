"""
Poker theory and hand ranges.
"""
from typing import Set, List
from ..core import Card, Position, get_hand_notation


# Preflop opening ranges by position (simplified GTO ranges)
# Format: Set of hand notations (e.g., "AA", "AKs", "AKo")

OPENING_RANGES = {
    Position.UTG: {
        # Tight range ~15% of hands
        "AA", "KK", "QQ", "JJ", "TT", "99",
        "AKs", "AQs", "AJs", "ATs",
        "AKo", "AQo",
        "KQs", "KJs",
    },
    Position.UTG1: {
        # ~16% of hands
        "AA", "KK", "QQ", "JJ", "TT", "99", "88",
        "AKs", "AQs", "AJs", "ATs", "A9s",
        "AKo", "AQo", "AJo",
        "KQs", "KJs", "KTs",
        "QJs",
    },
    Position.UTG2: {
        # ~17% of hands
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s",
        "AKo", "AQo", "AJo",
        "KQs", "KJs", "KTs",
        "QJs", "QTs",
        "JTs",
    },
    Position.MP: {
        # ~18% of hands
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A5s",
        "AKo", "AQo", "AJo", "ATo",
        "KQs", "KJs", "KTs", "K9s",
        "QJs", "QTs",
        "JTs", "J9s",
        "T9s",
    },
    Position.MP1: {
        # ~20% of hands
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s",
        "AKo", "AQo", "AJo", "ATo",
        "KQs", "KJs", "KTs", "K9s",
        "QJs", "QTs", "Q9s",
        "JTs", "J9s",
        "T9s", "T8s",
        "98s",
    },
    Position.CO: {
        # ~25% of hands - wider range
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "AKo", "AQo", "AJo", "ATo", "A9o",
        "KQs", "KJs", "KTs", "K9s", "K8s",
        "KQo", "KJo",
        "QJs", "QTs", "Q9s",
        "JTs", "J9s", "J8s",
        "T9s", "T8s",
        "98s", "97s",
        "87s",
    },
    Position.BTN: {
        # ~45% of hands - very wide range
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o",
        "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
        "KQo", "KJo", "KTo", "K9o",
        "QJs", "QTs", "Q9s", "Q8s", "Q7s",
        "QJo", "QTo",
        "JTs", "J9s", "J8s", "J7s",
        "JTo", "J9o",
        "T9s", "T8s", "T7s",
        "T9o",
        "98s", "97s", "96s",
        "98o",
        "87s", "86s",
        "76s",
        "65s",
    },
    Position.SB: {
        # Similar to CO but tighter due to bad post-flop position
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "AKo", "AQo", "AJo", "ATo", "A9o",
        "KQs", "KJs", "KTs", "K9s",
        "KQo", "KJo",
        "QJs", "QTs", "Q9s",
        "JTs", "J9s",
        "T9s", "T8s",
        "98s",
        "87s",
    },
    Position.BB: {
        # Defense range (when facing a raise, not opening)
        # For now, using similar to SB
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "AKo", "AQo", "AJo", "ATo", "A9o",
        "KQs", "KJs", "KTs", "K9s",
        "KQo", "KJo",
        "QJs", "QTs", "Q9s",
        "JTs", "J9s",
        "T9s", "T8s",
        "98s",
        "87s",
    },
}


def is_in_opening_range(hand_notation: str, position: Position) -> bool:
    """
    Check if a hand is in the opening range for a position.

    Args:
        hand_notation: Hand notation (e.g., "AKs", "QQ")
        position: Position to check

    Returns:
        True if hand should be played from this position
    """
    range_for_position = OPENING_RANGES.get(position, set())
    return hand_notation in range_for_position


def get_hand_strength_tier(hand_notation: str) -> int:
    """
    Get hand strength tier (1 = premium, 5 = trash).

    Args:
        hand_notation: Hand notation (e.g., "AA", "AKs", "72o")

    Returns:
        Tier from 1 (best) to 5 (worst)
    """
    # Tier 1: Premium hands
    tier1 = {"AA", "KK", "QQ", "AKs", "AKo"}

    # Tier 2: Strong hands
    tier2 = {"JJ", "TT", "99", "AQs", "AJs", "AQo", "KQs", "AJo"}

    # Tier 3: Playable hands
    tier3 = {
        "88", "77", "66", "55",
        "ATs", "A9s", "A8s",
        "KJs", "KTs", "KQo",
        "QJs", "QTs",
        "JTs",
    }

    # Tier 4: Marginal hands
    tier4 = {
        "44", "33", "22",
        "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "ATo", "A9o",
        "K9s", "K8s",
        "KJo", "KTo",
        "Q9s", "QJo",
        "J9s", "JTo",
        "T9s", "T8s",
        "98s", "97s",
        "87s", "86s",
        "76s", "75s",
        "65s",
    }

    # Tier 5: Weak/trash hands (everything else)

    if hand_notation in tier1:
        return 1
    elif hand_notation in tier2:
        return 2
    elif hand_notation in tier3:
        return 3
    elif hand_notation in tier4:
        return 4
    else:
        return 5


def should_open_raise(hole_cards: List[Card], position: Position) -> bool:
    """
    Determine if hero should open raise with this hand from this position.

    Args:
        hole_cards: Hero's two hole cards
        position: Hero's position

    Returns:
        True if hand should be opened
    """
    hand_notation = get_hand_notation(hole_cards)
    return is_in_opening_range(hand_notation, position)


def calculate_pot_odds(pot_size: float, bet_to_call: float) -> float:
    """
    Calculate pot odds as a ratio.

    Args:
        pot_size: Current pot size
        bet_to_call: Amount to call

    Returns:
        Pot odds as decimal (e.g., 0.33 = 3:1 = 33% pot odds)
    """
    if bet_to_call == 0:
        return 0.0
    return bet_to_call / (pot_size + bet_to_call)
