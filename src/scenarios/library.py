"""
Library of pre-built training scenarios.
"""
from typing import List
from .scenario import Scenario, create_simple_scenario, PlayerAction, Action
from ..core import Position


def get_beginner_scenarios() -> List[Scenario]:
    """Get beginner-level scenarios (basic preflop decisions)."""
    scenarios = []

    # Scenario 1: Premium hand on the button (6-max table)
    # Positions: UTG, MP, CO, BTN (you), SB, BB
    s1 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Ah",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have pocket aces on the button. Everyone folded to you.",
    )
    s1.name = "Premium Pocket Aces (6-max)"
    s1.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.CO, Action.FOLD),
    ]
    s1.difficulty = "beginner"
    s1.tags = ["preflop", "premium", "position", "6max"]
    scenarios.append(s1)

    # Scenario 2: Weak hand UTG (6-max) - first to act preflop
    s2 = create_simple_scenario(
        hero_position=Position.UTG,
        hero_cards_str="7h 2d",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have 7-2 offsuit in UTG. You're first to act preflop.",
    )
    s2.name = "Weak Hand UTG (6-max)"
    s2.action_history = []  # First to act, no prior action
    s2.difficulty = "beginner"
    s2.tags = ["preflop", "trash", "position", "6max"]
    scenarios.append(s2)

    # Scenario 3: Medium suited connector on button (6-max)
    s3 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="9h 8h",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have 9-8 suited on the button. Everyone folded to you.",
    )
    s3.name = "Suited Connector BTN (6-max)"
    s3.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.CO, Action.FOLD),
    ]
    s3.difficulty = "beginner"
    s3.tags = ["preflop", "suited_connector", "position", "6max"]
    scenarios.append(s3)

    # Scenario 4: AK on button facing UTG raise (6-max)
    s4 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="As Kd",
        pot_size=4.5,
        current_bet=3.0,
        description="6-max table. You have AK offsuit on the button. UTG raised to 3BB, others folded.",
    )
    s4.action_history = [
        PlayerAction(Position.UTG, Action.RAISE, 3.0),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.CO, Action.FOLD),
    ]
    s4.name = "AK Facing Raise (6-max)"
    s4.difficulty = "beginner"
    s4.tags = ["preflop", "facing_raise", "premium", "6max"]
    scenarios.append(s4)

    # Scenario 5: Small pocket pair in MP (6-max) - unopened
    s5 = create_simple_scenario(
        hero_position=Position.MP,
        hero_cards_str="6d 6c",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have pocket sixes in MP. UTG folded.",
    )
    s5.name = "66 in MP Unopened (6-max)"
    s5.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
    ]
    s5.difficulty = "beginner"
    s5.tags = ["preflop", "pocket_pair", "position", "6max"]
    scenarios.append(s5)

    # Scenario 6: Same hand (66) but facing UTG raise (6-max)
    s6 = create_simple_scenario(
        hero_position=Position.MP,
        hero_cards_str="6d 6c",
        pot_size=4.5,
        current_bet=3.0,
        description="6-max table. You have pocket sixes in MP. UTG raised to 3BB.",
    )
    s6.name = "66 Facing Raise (6-max)"
    s6.action_history = [
        PlayerAction(Position.UTG, Action.RAISE, 3.0),
    ]
    s6.difficulty = "beginner"
    s6.tags = ["preflop", "pocket_pair", "facing_raise", "6max"]
    scenarios.append(s6)

    return scenarios


def get_intermediate_scenarios() -> List[Scenario]:
    """Get intermediate-level scenarios (6-max)."""
    scenarios = []

    # Scenario 1: A5s in UTG (6-max) - marginal suited ace
    s1 = create_simple_scenario(
        hero_position=Position.UTG,
        hero_cards_str="Ad 5d",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have A5 suited in UTG. You're first to act.",
    )
    s1.name = "A5s UTG (6-max)"
    s1.action_history = []  # First to act
    s1.difficulty = "intermediate"
    s1.tags = ["preflop", "suited_ace", "position", "6max"]
    scenarios.append(s1)

    # Scenario 2: JJ in CO facing BTN 3-bet (6-max)
    s2 = create_simple_scenario(
        hero_position=Position.CO,
        hero_cards_str="Jh Jd",
        pot_size=10.5,
        current_bet=9.0,
        description="6-max table. You raised from CO to 3BB. BTN 3-bet to 9BB.",
    )
    s2.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
        PlayerAction(Position.CO, Action.RAISE, 3.0),
        PlayerAction(Position.BTN, Action.RAISE, 9.0),
    ]
    s2.name = "JJ Facing 3-Bet (6-max)"
    s2.difficulty = "intermediate"
    s2.tags = ["preflop", "facing_3bet", "pocket_pair", "6max"]
    scenarios.append(s2)

    # Scenario 3: KQo in CO (6-max) - unopened
    s3 = create_simple_scenario(
        hero_position=Position.CO,
        hero_cards_str="Kc Qh",
        pot_size=1.5,
        current_bet=0.0,
        description="6-max table. You have KQ offsuit in the CO. UTG and MP folded.",
    )
    s3.name = "KQo in CO (6-max)"
    s3.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.MP, Action.FOLD),
    ]
    s3.difficulty = "intermediate"
    s3.tags = ["preflop", "broadway", "position", "6max"]
    scenarios.append(s3)

    # Scenario 4: AQo on BTN facing MP raise + CO call (6-max multiway)
    s4 = create_simple_scenario(
        hero_position=Position.BTN,
        hero_cards_str="Ah Qc",
        pot_size=7.5,
        current_bet=3.0,
        description="6-max table. You have AQ offsuit on BTN. MP raised to 3BB, CO called.",
    )
    s4.name = "AQo Multiway (6-max)"
    s4.action_history = [
        PlayerAction(Position.UTG, Action.FOLD),
        PlayerAction(Position.MP, Action.RAISE, 3.0),
        PlayerAction(Position.CO, Action.CALL),
    ]
    s4.difficulty = "intermediate"
    s4.tags = ["preflop", "facing_raise", "multiway", "6max"]
    scenarios.append(s4)

    return scenarios


def get_all_scenarios() -> List[Scenario]:
    """Get all available scenarios."""
    return get_beginner_scenarios() + get_intermediate_scenarios()


def get_scenarios_by_difficulty(difficulty: str) -> List[Scenario]:
    """Get scenarios filtered by difficulty."""
    all_scenarios = get_all_scenarios()
    return [s for s in all_scenarios if s.difficulty == difficulty]
