"""
Library of pre-built training scenarios.
"""
from typing import List
from .scenario import Scenario, create_simple_scenario, PlayerAction, Action
from ..core import Position


def get_beginner_scenarios() -> List[Scenario]:
    """Get beginner-level scenarios (basic preflop decisions)."""
    scenarios = []

    # Scenario 1: Premium hand in late position
    s1 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Ah",
        pot_size=1.5,
        current_bet=0.0,
        description="You have pocket aces on the button. No one has acted yet.",
    )
    s1.name = "Premium Pocket Aces"
    s1.difficulty = "beginner"
    s1.tags = ["preflop", "premium", "position"]
    scenarios.append(s1)

    # Scenario 2: Weak hand in early position
    s2 = create_simple_scenario(
        hero_position=Position.UTG,
        hero_cards_str="7h 2d",
        pot_size=1.5,
        current_bet=0.0,
        description="You have 7-2 offsuit under the gun. No one has acted.",
    )
    s2.name = "Weak Hand Early Position"
    s2.difficulty = "beginner"
    s2.tags = ["preflop", "trash", "position"]
    scenarios.append(s2)

    # Scenario 3: Medium suited connector on button - everyone folded
    s3 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="9h 8h",
        pot_size=1.5,
        current_bet=0.0,
        description="You have 9-8 suited on the button. Everyone folded to you.",
    )
    s3.name = "Suited Connector Button (Unopened)"
    s3.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.UTG1, Action.FOLD),
        PlayerAction(Position.UTG2, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.MP1, Action.FOLD),
        PlayerAction(Position.CO, Action.FOLD),
    ]
    s3.difficulty = "beginner"
    s3.tags = ["preflop", "suited_connector", "position"]
    scenarios.append(s3)

    # Scenario 4: Facing a raise with AK
    s4 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Kd",
        pot_size=4.5,
        current_bet=3.0,
        description="You have AK offsuit on the button. UTG raised to 3BB.",
    )
    s4.action_history = [
        PlayerAction(Position.UTG, Action.RAISE, 3.0)
    ]
    s4.name = "AK Facing Raise"
    s4.difficulty = "beginner"
    s4.tags = ["preflop", "facing_raise", "premium"]
    scenarios.append(s4)

    # Scenario 5: Small pocket pair in middle position - unopened
    s5 = create_simple_scenario(
        hero_position=Position.MP,
        hero_cards_str="6d 6c",
        pot_size=1.5,
        current_bet=0.0,
        description="You have pocket sixes in middle position. Everyone folded to you.",
    )
    s5.name = "Small Pocket Pair MP (Unopened)"
    s5.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.UTG1, Action.FOLD),
        PlayerAction(Position.UTG2, Action.FOLD),
    ]
    s5.difficulty = "beginner"
    s5.tags = ["preflop", "pocket_pair", "position"]
    scenarios.append(s5)

    # Scenario 6: Same hand but facing a raise - totally different!
    s6 = create_simple_scenario(
        hero_position=Position.MP,
        hero_cards_str="6d 6c",
        pot_size=4.5,
        current_bet=3.0,
        description="You have pocket sixes in middle position. UTG raised to 3BB.",
    )
    s6.name = "Small Pocket Pair Facing Raise"
    s6.action_history = [
        PlayerAction(Position.UTG, Action.RAISE, 3.0),
        PlayerAction(Position.UTG1, Action.FOLD),
        PlayerAction(Position.UTG2, Action.FOLD),
    ]
    s6.difficulty = "beginner"
    s6.tags = ["preflop", "pocket_pair", "facing_raise"]
    scenarios.append(s6)

    return scenarios


def get_intermediate_scenarios() -> List[Scenario]:
    """Get intermediate-level scenarios."""
    scenarios = []

    # Scenario 1: Ace-rag suited in early position
    s1 = create_simple_scenario(
        hero_position=Position.UTG1,
        hero_cards_str="Ad 5d",
        pot_size=1.5,
        current_bet=0.0,
        description="You have A5 suited in early position.",
    )
    s1.name = "Ace-X Suited Early"
    s1.difficulty = "intermediate"
    s1.tags = ["preflop", "suited_ace", "position"]
    scenarios.append(s1)

    # Scenario 2: Facing 3-bet with JJ
    s2 = create_simple_scenario(
        hero_position=Position.CO,
        hero_cards_str="Jh Jd",
        pot_size=10.5,
        current_bet=9.0,
        description="You raised from CO, BTN 3-bet to 9BB.",
    )
    s2.action_history = [
        PlayerAction(Position.CO, Action.RAISE, 3.0),
        PlayerAction(Position.BTN, Action.RAISE, 9.0),
    ]
    s2.name = "JJ Facing 3-Bet"
    s2.difficulty = "intermediate"
    s2.tags = ["preflop", "facing_3bet", "pocket_pair"]
    scenarios.append(s2)

    # Scenario 3: King-Queen offsuit in cutoff - everyone folded
    s3 = create_simple_scenario(
        hero_position=Position.CO,
        hero_cards_str="Kc Qh",
        pot_size=1.5,
        current_bet=0.0,
        description="You have KQ offsuit in the cutoff. Everyone folded to you.",
    )
    s3.name = "KQ Offsuit CO (Unopened)"
    s3.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.UTG1, Action.FOLD),
        PlayerAction(Position.UTG2, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.MP1, Action.FOLD),
    ]
    s3.difficulty = "intermediate"
    s3.tags = ["preflop", "broadway", "position"]
    scenarios.append(s3)

    # Scenario 4: AQ facing raise and a call - multiway pot
    s4 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="Ah Qc",
        pot_size=7.5,
        current_bet=3.0,
        description="You have AQ offsuit on the button. MP raised to 3BB, CO called.",
    )
    s4.name = "AQ Multiway (Raise + Call)"
    s4.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.UTG1, Action.FOLD),
        PlayerAction(Position.UTG2, Action.FOLD),
        PlayerAction(Position.MP, Action.RAISE, 3.0),
        PlayerAction(Position.MP1, Action.FOLD),
        PlayerAction(Position.CO, Action.CALL),
    ]
    s4.difficulty = "intermediate"
    s4.tags = ["preflop", "facing_raise", "multiway"]
    scenarios.append(s4)

    return scenarios


def get_all_scenarios() -> List[Scenario]:
    """Get all available scenarios."""
    return get_beginner_scenarios() + get_intermediate_scenarios()


def get_scenarios_by_difficulty(difficulty: str) -> List[Scenario]:
    """Get scenarios filtered by difficulty."""
    all_scenarios = get_all_scenarios()
    return [s for s in all_scenarios if s.difficulty == difficulty]
