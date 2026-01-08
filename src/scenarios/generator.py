"""
Scenario generator - creates randomized but realistic poker scenarios.
"""
import random
from typing import List, Optional
from dataclasses import dataclass

from ..core import Deck, Card, Position, parse_cards
from .scenario import Scenario, Action, PlayerAction, Street


@dataclass
class DifficultyConfig:
    """Configuration for scenario difficulty."""
    name: str
    # Hand strength distributions (what % of hands are premium/good/marginal/trash)
    hand_strength_weights: dict  # {tier: weight}
    # Position distributions
    position_weights: dict  # {position: weight}
    # Action complexity (how many players acted before)
    max_prior_actions: int
    min_prior_actions: int
    # Facing raises/3bets
    raise_frequency: float  # 0.0 to 1.0
    three_bet_frequency: float


# Difficulty presets
DIFFICULTY_CONFIGS = {
    'beginner': DifficultyConfig(
        name='beginner',
        hand_strength_weights={1: 0.3, 2: 0.3, 3: 0.2, 4: 0.15, 5: 0.05},  # More premium hands
        position_weights={
            Position.UTG: 0.1,
            Position.MP: 0.15,
            Position.CO: 0.25,
            Position.BTN: 0.35,  # Favor easier positions
            Position.SB: 0.05,
            Position.BB: 0.10,
        },
        max_prior_actions=2,
        min_prior_actions=0,
        raise_frequency=0.3,
        three_bet_frequency=0.0,
    ),
    'intermediate': DifficultyConfig(
        name='intermediate',
        hand_strength_weights={1: 0.2, 2: 0.25, 3: 0.25, 4: 0.2, 5: 0.1},  # More mixed
        position_weights={
            Position.UTG: 0.15,
            Position.MP: 0.2,
            Position.CO: 0.25,
            Position.BTN: 0.25,
            Position.SB: 0.05,
            Position.BB: 0.10,
        },
        max_prior_actions=3,
        min_prior_actions=0,
        raise_frequency=0.5,
        three_bet_frequency=0.15,
    ),
    'advanced': DifficultyConfig(
        name='advanced',
        hand_strength_weights={1: 0.15, 2: 0.2, 3: 0.25, 4: 0.25, 5: 0.15},  # More marginal
        position_weights={
            Position.UTG: 0.2,
            Position.MP: 0.2,
            Position.CO: 0.2,
            Position.BTN: 0.2,
            Position.SB: 0.1,
            Position.BB: 0.1,
        },
        max_prior_actions=5,
        min_prior_actions=1,
        raise_frequency=0.6,
        three_bet_frequency=0.25,
    ),
}


class ScenarioGenerator:
    """Generates random but realistic poker scenarios."""

    def __init__(self):
        self.deck = Deck()

    def generate(self, difficulty: str = 'beginner') -> Scenario:
        """Generate a random scenario based on difficulty."""
        config = DIFFICULTY_CONFIGS.get(difficulty, DIFFICULTY_CONFIGS['beginner'])

        # Reset deck
        self.deck.reset()
        self.deck.shuffle()

        # Choose position based on difficulty weights
        hero_position = random.choices(
            list(config.position_weights.keys()),
            weights=list(config.position_weights.values()),
            k=1
        )[0]

        # Deal hero cards - weighted by difficulty
        hero_cards = self._generate_hand(config)

        # Generate action before hero
        action_history = self._generate_action_history(
            hero_position, config
        )

        # Calculate pot and current bet from action
        pot_size, current_bet = self._calculate_pot_and_bet(action_history)

        # Create scenario
        scenario = Scenario(
            name=self._generate_name(hero_position, hero_cards, action_history),
            description=f"6-max table. {self._generate_description(hero_position, action_history)}",
            street=Street.PREFLOP,
            hero_position=hero_position,
            hero_cards=hero_cards,
            board_cards=[],
            action_history=action_history,
            pot_size=pot_size,
            current_bet=current_bet,
            difficulty=difficulty,
            tags=['preflop', '6max', 'generated'],
        )

        return scenario

    def _generate_hand(self, config: DifficultyConfig) -> List[Card]:
        """Generate hero's hand based on difficulty."""
        from ..grading.theory import get_hand_strength_tier
        from ..core import get_hand_notation

        # Try up to 50 times to get a hand matching our tier distribution
        for _ in range(50):
            deck_copy = Deck()
            deck_copy.shuffle()
            cards = deck_copy.deal(2)
            hand_notation = get_hand_notation(cards)
            tier = get_hand_strength_tier(hand_notation)

            # Check if this tier matches our distribution
            if random.random() < config.hand_strength_weights.get(tier, 0) * 5:
                return cards

        # Fallback - just deal random cards
        return self.deck.deal(2)

    def _generate_action_history(
        self, hero_position: Position, config: DifficultyConfig
    ) -> List[PlayerAction]:
        """Generate realistic action before hero."""
        # Get positions that act before hero
        positions_before = self._get_positions_before(hero_position)

        if not positions_before:
            return []  # Hero is first to act

        action_history = []

        # Determine if there's a raise
        has_raise = random.random() < config.raise_frequency
        raise_position = None

        for pos in positions_before:
            if has_raise and raise_position is None and random.random() < 0.4:
                # This position raises
                action_history.append(
                    PlayerAction(pos, Action.RAISE, 3.0)
                )
                raise_position = pos
            elif raise_position:
                # After a raise, decide to fold/call/3bet
                if random.random() < config.three_bet_frequency and len(action_history) < 3:
                    # 3-bet
                    action_history.append(
                        PlayerAction(pos, Action.RAISE, 9.0)
                    )
                    raise_position = pos  # Update raise position
                elif random.random() < 0.2:
                    # Call
                    action_history.append(
                        PlayerAction(pos, Action.CALL)
                    )
                else:
                    # Fold
                    action_history.append(
                        PlayerAction(pos, Action.FOLD)
                    )
            else:
                # No raise yet, just fold
                action_history.append(
                    PlayerAction(pos, Action.FOLD)
                )

        return action_history

    def _get_positions_before(self, hero_position: Position) -> List[Position]:
        """Get positions that act before hero in 6-max."""
        # 6-max order: UTG, MP, CO, BTN, SB, BB (preflop)
        order_6max = [
            Position.UTG,
            Position.MP,
            Position.CO,
            Position.BTN,
            Position.SB,
            Position.BB,
        ]

        try:
            hero_index = order_6max.index(hero_position)
            return order_6max[:hero_index]
        except ValueError:
            return []

    def _calculate_pot_and_bet(self, action_history: List[PlayerAction]) -> tuple:
        """Calculate pot size and current bet from action history."""
        pot = 1.5  # Blinds
        current_bet = 0.0

        for action in action_history:
            if action.action == Action.RAISE:
                pot += current_bet  # Previous bet goes to pot
                current_bet = action.amount or 3.0
                pot += current_bet  # Raiser's bet goes to pot
            elif action.action == Action.CALL:
                pot += current_bet  # Caller matches current bet

        return pot, current_bet

    def _generate_name(
        self, position: Position, cards: List[Card], action_history: List[PlayerAction]
    ) -> str:
        """Generate a descriptive name for the scenario."""
        from ..core import get_hand_notation

        hand = get_hand_notation(cards)

        # Check if facing raise
        has_raise = any(a.action == Action.RAISE for a in action_history)
        has_3bet = sum(a.action == Action.RAISE for a in action_history) >= 2
        has_call = any(a.action == Action.CALL for a in action_history)

        if has_3bet:
            return f"{hand} in {position.abbr} facing 3-bet"
        elif has_raise and has_call:
            return f"{hand} in {position.abbr} multiway"
        elif has_raise:
            return f"{hand} in {position.abbr} facing raise"
        else:
            return f"{hand} in {position.abbr} (unopened)"

    def _generate_description(
        self, position: Position, action_history: List[PlayerAction]
    ) -> str:
        """Generate description text."""
        if not action_history:
            return f"You're in {position.full_name}. You're first to act."

        # Summarize action
        raises = [a for a in action_history if a.action == Action.RAISE]
        calls = [a for a in action_history if a.action == Action.CALL]

        if len(raises) >= 2:
            return f"{raises[0].position.abbr} raised, {raises[1].position.abbr} 3-bet."
        elif raises and calls:
            return f"{raises[0].position.abbr} raised, {calls[0].position.abbr} called."
        elif raises:
            return f"{raises[0].position.abbr} raised to {raises[0].amount}BB."
        else:
            return f"Everyone folded to you in {position.full_name}."


def generate_batch(difficulty: str, count: int) -> List[Scenario]:
    """Generate multiple scenarios at once."""
    generator = ScenarioGenerator()
    return [generator.generate(difficulty) for _ in range(count)]
