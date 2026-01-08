"""
Decision grading and evaluation engine.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict

from ..scenarios.scenario import Scenario, Action, Street
from ..core import Position, get_hand_notation
from .theory import (
    should_open_raise,
    is_in_opening_range,
    get_hand_strength_tier,
    calculate_pot_odds,
)


class Grade(Enum):
    """Decision grades from best to worst."""
    EXCELLENT = (5, "Excellent", "The best or one of the best moves")
    GOOD = (4, "Good", "A solid move, close to optimal")
    INACCURATE = (3, "Inaccurate", "Playable but not ideal")
    MISTAKE = (2, "Mistake", "A clear error")
    BLUNDER = (1, "Blunder", "A serious mistake")

    def __init__(self, grade_value: int, label: str, description: str):
        self.grade_value = grade_value
        self.label = label
        self.description = description

    def __str__(self):
        return self.label

    def __lt__(self, other):
        return self.grade_value < other.grade_value


@dataclass
class DecisionEvaluation:
    """Result of evaluating a player's decision."""
    chosen_action: Action
    grade: Grade
    best_action: Action
    explanation: str
    alternative_actions: Dict[Action, Grade] = None  # Other actions and their grades

    def __post_init__(self):
        if self.alternative_actions is None:
            self.alternative_actions = {}

    def get_summary(self) -> str:
        """Get human-readable summary."""
        lines = [
            f"Your action: {self.chosen_action.value}",
            f"Grade: {self.grade.label}",
            f"Best action: {self.best_action.value}",
            f"\n{self.explanation}",
        ]
        return "\n".join(lines)


class DecisionEvaluator:
    """Evaluates poker decisions based on theory."""

    def evaluate_decision(
        self,
        scenario: Scenario,
        chosen_action: Action,
    ) -> DecisionEvaluation:
        """
        Evaluate a player's decision in a scenario.

        Args:
            scenario: The poker scenario
            chosen_action: The action the player chose

        Returns:
            DecisionEvaluation with grade and explanation
        """
        # For now, focus on preflop decisions
        if scenario.street == Street.PREFLOP:
            return self._evaluate_preflop(scenario, chosen_action)
        else:
            # Post-flop evaluation (simplified for now)
            return self._evaluate_postflop(scenario, chosen_action)

    def _evaluate_preflop(
        self,
        scenario: Scenario,
        chosen_action: Action,
    ) -> DecisionEvaluation:
        """Evaluate preflop decision."""
        hand_notation = get_hand_notation(scenario.hero_cards)
        position = scenario.hero_position
        in_range = is_in_opening_range(hand_notation, position)
        hand_tier = get_hand_strength_tier(hand_notation)

        # Check if this is an opening situation (no prior action)
        is_opening = len(scenario.action_history) == 0 and scenario.current_bet == 0

        if is_opening:
            return self._evaluate_opening(
                scenario, chosen_action, hand_notation, position, in_range, hand_tier
            )
        else:
            return self._evaluate_facing_raise(
                scenario, chosen_action, hand_notation, position, in_range, hand_tier
            )

    def _evaluate_opening(
        self,
        scenario: Scenario,
        chosen_action: Action,
        hand_notation: str,
        position: Position,
        in_range: bool,
        hand_tier: int,
    ) -> DecisionEvaluation:
        """Evaluate opening decision (no one has acted yet)."""

        # Determine best action
        if in_range:
            best_action = Action.RAISE
        else:
            best_action = Action.FOLD

        # Grade the chosen action
        if chosen_action == best_action:
            grade = Grade.EXCELLENT
            explanation = self._get_opening_explanation(
                hand_notation, position, in_range, hand_tier, True
            )
        elif chosen_action == Action.RAISE and not in_range:
            # Raising with out-of-range hand
            if hand_tier <= 3:
                grade = Grade.INACCURATE
                explanation = f"{hand_notation} is marginal from {position}. Folding is more standard, but raising can work."
            else:
                grade = Grade.MISTAKE
                explanation = f"{hand_notation} is too weak to raise from {position}. This hand should be folded."
        elif chosen_action == Action.FOLD and in_range:
            # Folding an in-range hand
            if hand_tier == 1:
                grade = Grade.BLUNDER
                explanation = f"Folding {hand_notation} is a serious mistake! This is a premium hand that should always be raised."
            elif hand_tier == 2:
                grade = Grade.MISTAKE
                explanation = f"{hand_notation} is a strong hand that should be raised from {position}."
            else:
                grade = Grade.INACCURATE
                explanation = f"{hand_notation} should be raised from {position}, though it's not a critical error to fold."
        elif chosen_action == Action.CALL:
            # Limping (calling without a raise)
            grade = Grade.MISTAKE
            explanation = "Limping (just calling) is generally weak play. You should either raise or fold."
        else:
            grade = Grade.MISTAKE
            explanation = f"Unexpected action for this situation."

        return DecisionEvaluation(
            chosen_action=chosen_action,
            grade=grade,
            best_action=best_action,
            explanation=explanation,
        )

    def _evaluate_facing_raise(
        self,
        scenario: Scenario,
        chosen_action: Action,
        hand_notation: str,
        position: Position,
        in_range: bool,
        hand_tier: int,
    ) -> DecisionEvaluation:
        """Evaluate decision when facing a raise."""

        # Simplified: premium hands should re-raise or call, others fold
        pot_odds = calculate_pot_odds(scenario.pot_size, scenario.current_bet)

        if hand_tier == 1:
            # Premium hands: should re-raise
            best_action = Action.RAISE
            if chosen_action == Action.RAISE:
                grade = Grade.EXCELLENT
                explanation = f"{hand_notation} is premium. Re-raising is the best play."
            elif chosen_action == Action.CALL:
                grade = Grade.GOOD
                explanation = f"Calling with {hand_notation} is acceptable, though re-raising is more aggressive."
            else:
                grade = Grade.BLUNDER
                explanation = f"Never fold {hand_notation} to a single raise! This is a premium hand."
        elif hand_tier == 2:
            # Strong hands: can call or re-raise
            best_action = Action.CALL
            if chosen_action in [Action.CALL, Action.RAISE]:
                grade = Grade.EXCELLENT if chosen_action == Action.CALL else Grade.GOOD
                explanation = f"{hand_notation} is strong enough to continue."
            else:
                grade = Grade.MISTAKE
                explanation = f"{hand_notation} is too strong to fold to a single raise."
        elif hand_tier == 3:
            # Playable hands: depends on pot odds and position
            if pot_odds < 0.25:  # Getting good odds
                best_action = Action.CALL
                if chosen_action == Action.CALL:
                    grade = Grade.GOOD
                    explanation = f"{hand_notation} can call with good pot odds ({pot_odds:.1%})."
                elif chosen_action == Action.FOLD:
                    grade = Grade.INACCURATE
                    explanation = f"Folding is acceptable but you're getting good odds to call."
                else:
                    grade = Grade.INACCURATE
                    explanation = f"Re-raising {hand_notation} is aggressive but can work."
            else:
                best_action = Action.FOLD
                if chosen_action == Action.FOLD:
                    grade = Grade.EXCELLENT
                    explanation = f"{hand_notation} is marginal. Folding is correct with poor odds."
                else:
                    grade = Grade.INACCURATE
                    explanation = f"Calling is loose here, but not terrible."
        else:
            # Weak hands: should fold
            best_action = Action.FOLD
            if chosen_action == Action.FOLD:
                grade = Grade.EXCELLENT
                explanation = f"{hand_notation} is too weak to continue. Easy fold."
            else:
                grade = Grade.MISTAKE
                explanation = f"{hand_notation} is not strong enough to call a raise."

        return DecisionEvaluation(
            chosen_action=chosen_action,
            grade=grade,
            best_action=best_action,
            explanation=explanation,
        )

    def _evaluate_postflop(
        self,
        scenario: Scenario,
        chosen_action: Action,
    ) -> DecisionEvaluation:
        """
        Simplified post-flop evaluation.

        This is a placeholder for now. Full post-flop evaluation would require:
        - Hand equity calculation
        - Board texture analysis
        - Range analysis
        - Bet sizing theory
        """
        # For now, provide generic feedback
        return DecisionEvaluation(
            chosen_action=chosen_action,
            grade=Grade.GOOD,
            best_action=chosen_action,
            explanation="Post-flop analysis is simplified for now. Full evaluation coming soon.",
        )

    def _get_opening_explanation(
        self,
        hand_notation: str,
        position: Position,
        in_range: bool,
        hand_tier: int,
        is_correct: bool,
    ) -> str:
        """Generate explanation for opening decision."""
        if is_correct and in_range:
            tier_descriptions = {
                1: "a premium hand",
                2: "a strong hand",
                3: "a playable hand",
                4: "a marginal hand",
            }
            return (
                f"Excellent! {hand_notation} is {tier_descriptions.get(hand_tier, 'playable')} "
                f"and should be raised from {position}."
            )
        elif is_correct and not in_range:
            return f"Correct fold. {hand_notation} is too weak to open from {position}."
        else:
            return "Unexpected action."
