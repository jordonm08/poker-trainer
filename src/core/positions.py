"""
Poker position definitions and analysis.
"""
from enum import Enum


class Position(Enum):
    """
    Poker positions at a standard 9-handed table.

    Order from earliest to latest position:
    UTG (Under the Gun) - earliest position
    UTG+1, UTG+2 - early position
    MP (Middle Position) - middle position
    MP+1 - late middle position
    CO (Cutoff) - late position
    BTN (Button) - latest position (best position)
    SB (Small Blind) - special (acts last pre-flop, first post-flop)
    BB (Big Blind) - special (acts last pre-flop in the first round)
    """
    UTG = ("UTG", "Under the Gun", 1, "early")
    UTG1 = ("UTG+1", "Under the Gun +1", 2, "early")
    UTG2 = ("UTG+2", "Under the Gun +2", 3, "early")
    MP = ("MP", "Middle Position", 4, "middle")
    MP1 = ("MP+1", "Middle Position +1", 5, "middle")
    CO = ("CO", "Cutoff", 6, "late")
    BTN = ("BTN", "Button", 7, "late")
    SB = ("SB", "Small Blind", 8, "blind")
    BB = ("BB", "Big Blind", 9, "blind")

    def __init__(self, abbr: str, full_name: str, order: int, category: str):
        self.abbr = abbr
        self.full_name = full_name
        self.order = order  # Lower is earlier position
        self.category = category

    def is_early_position(self) -> bool:
        """Check if this is an early position."""
        return self.category == "early"

    def is_middle_position(self) -> bool:
        """Check if this is a middle position."""
        return self.category == "middle"

    def is_late_position(self) -> bool:
        """Check if this is a late position."""
        return self.category == "late"

    def is_blind(self) -> bool:
        """Check if this is a blind position."""
        return self.category == "blind"

    def __str__(self) -> str:
        return self.abbr

    def __repr__(self) -> str:
        return f"Position.{self.name}"


def get_position_strength(position: Position) -> float:
    """
    Get relative strength of a position (0.0 to 1.0).

    Higher values indicate better positions (more information, act later).

    Args:
        position: Position to evaluate

    Returns:
        Float between 0.0 and 1.0
    """
    # Button is strongest (1.0), UTG is weakest (0.0)
    # Blinds have special consideration as they act last pre-flop but first post-flop
    strength_map = {
        Position.UTG: 0.0,
        Position.UTG1: 0.15,
        Position.UTG2: 0.25,
        Position.MP: 0.35,
        Position.MP1: 0.50,
        Position.CO: 0.70,
        Position.BTN: 1.0,
        Position.SB: 0.20,  # Bad position post-flop
        Position.BB: 0.30,  # Slightly better than SB, gets to close action pre-flop
    }
    return strength_map[position]


def positions_between(pos1: Position, pos2: Position) -> int:
    """
    Calculate number of positions between two players.

    Args:
        pos1: First position
        pos2: Second position

    Returns:
        Number of positions between them
    """
    return abs(pos1.order - pos2.order)
