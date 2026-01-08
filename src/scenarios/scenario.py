"""
Poker scenario representation and management.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

from ..core import Card, Position, parse_cards


class Action(Enum):
    """Possible poker actions."""
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"

    def __str__(self):
        return self.value


class Street(Enum):
    """Betting rounds."""
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"

    def __str__(self):
        return self.value


@dataclass
class PlayerAction:
    """Represents an action taken by a player."""
    position: Position
    action: Action
    amount: Optional[float] = None  # Bet/raise amount (in big blinds)

    def __str__(self) -> str:
        if self.amount is not None:
            return f"{self.position} {self.action.value} {self.amount}BB"
        return f"{self.position} {self.action.value}"


@dataclass
class Scenario:
    """
    Represents a poker training scenario.

    A scenario presents a specific situation and asks the player to make a decision.
    """
    # Identification
    id: Optional[int] = None
    name: str = ""
    description: str = ""

    # Game state
    street: Street = Street.PREFLOP
    hero_position: Position = Position.BTN
    hero_cards: List[Card] = None
    board_cards: List[Card] = None  # Empty for preflop

    # Action history
    action_history: List[PlayerAction] = None

    # Pot state
    pot_size: float = 1.5  # In big blinds
    current_bet: float = 0.0  # Current bet to call (in big blinds)

    # Available actions for hero
    available_actions: List[Action] = None

    # Metadata
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    tags: List[str] = None  # e.g., ["bluff", "value_bet", "pot_odds"]

    def __post_init__(self):
        """Initialize mutable defaults."""
        if self.hero_cards is None:
            self.hero_cards = []
        if self.board_cards is None:
            self.board_cards = []
        if self.action_history is None:
            self.action_history = []
        if self.available_actions is None:
            self.available_actions = self._determine_available_actions()
        if self.tags is None:
            self.tags = []

    def _determine_available_actions(self) -> List[Action]:
        """Determine what actions are available based on game state."""
        actions = [Action.FOLD]

        if self.current_bet == 0:
            # No bet to call, can check or raise (open)
            actions.append(Action.CHECK)
            actions.append(Action.RAISE)  # Opening is called a "raise" in poker
        else:
            # There's a bet, can call or raise
            actions.append(Action.CALL)
            actions.append(Action.RAISE)

        return actions

    def get_description_text(self) -> str:
        """Generate human-readable scenario description."""
        lines = []

        # Position and cards
        lines.append(f"Position: {self.hero_position.full_name}")
        if self.hero_cards:
            cards_str = " ".join(str(c) for c in self.hero_cards)
            lines.append(f"Your hand: {cards_str}")

        # Board
        if self.board_cards:
            board_str = " ".join(str(c) for c in self.board_cards)
            lines.append(f"Board: {board_str}")

        # Pot and bet
        lines.append(f"Pot: {self.pot_size}BB")
        if self.current_bet > 0:
            lines.append(f"Bet to call: {self.current_bet}BB")

        # Action history - always show what happened before you
        lines.append("\nAction before you:")
        if self.action_history and len(self.action_history) > 0:
            for action in self.action_history:
                lines.append(f"  {action}")
        else:
            lines.append(f"  (You are first to act)")

        return "\n".join(lines)

    def is_valid(self) -> bool:
        """Check if scenario is valid."""
        # Must have hero cards
        if not self.hero_cards or len(self.hero_cards) != 2:
            return False

        # Board cards must match street
        expected_board_cards = {
            Street.PREFLOP: 0,
            Street.FLOP: 3,
            Street.TURN: 4,
            Street.RIVER: 5,
        }

        if len(self.board_cards) != expected_board_cards[self.street]:
            return False

        return True


def create_simple_scenario(
    hero_position: Position,
    hero_cards_str: str,
    board_cards_str: str = "",
    pot_size: float = 1.5,
    current_bet: float = 0.0,
    description: str = "",
) -> Scenario:
    """
    Helper to create a scenario from string notation.

    Args:
        hero_position: Hero's position
        hero_cards_str: Hero cards (e.g., "As Kh")
        board_cards_str: Board cards (e.g., "Qd Jc Th")
        pot_size: Pot size in big blinds
        current_bet: Current bet in big blinds
        description: Scenario description

    Returns:
        Scenario object
    """
    hero_cards = parse_cards(hero_cards_str)
    board_cards = parse_cards(board_cards_str) if board_cards_str else []

    # Determine street from board
    street_map = {0: Street.PREFLOP, 3: Street.FLOP, 4: Street.TURN, 5: Street.RIVER}
    street = street_map.get(len(board_cards), Street.PREFLOP)

    return Scenario(
        hero_position=hero_position,
        hero_cards=hero_cards,
        board_cards=board_cards,
        street=street,
        pot_size=pot_size,
        current_bet=current_bet,
        description=description,
    )
