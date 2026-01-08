"""
Web interface for poker trainer using Flask.
"""
from flask import Flask, render_template, request, jsonify, session
import os
import secrets

from ..scenarios.library import get_beginner_scenarios, get_intermediate_scenarios
from ..scenarios.generator import ScenarioGenerator
from ..scenarios.adaptive import AdaptiveDifficulty
from ..grading.evaluator import DecisionEvaluator

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

evaluator = DecisionEvaluator()
generator = ScenarioGenerator()

# Store adaptive difficulty per session
adaptive_difficulties = {}


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/scenarios/<difficulty>')
def get_scenarios(difficulty):
    """Get scenarios by difficulty."""
    if difficulty == 'beginner':
        scenarios = get_beginner_scenarios()
    elif difficulty == 'intermediate':
        scenarios = get_intermediate_scenarios()
    else:
        return jsonify({'error': 'Invalid difficulty'}), 400

    # Convert scenarios to JSON-serializable format
    scenario_data = []
    for i, scenario in enumerate(scenarios):
        scenario_data.append({
            'id': i,
            'name': scenario.name,
            'description': scenario.description,
            'position': scenario.hero_position.abbr,
            'position_full': scenario.hero_position.full_name,
            'cards': [str(c) for c in scenario.hero_cards],
            'board': [str(c) for c in scenario.board_cards],
            'pot': scenario.pot_size,
            'current_bet': scenario.current_bet,
            'action_history': [
                {
                    'position': action.position.abbr,
                    'action': action.action.value,
                    'amount': action.amount
                }
                for action in scenario.action_history
            ],
            'available_actions': [action.value for action in scenario.available_actions]
        })

    return jsonify(scenario_data)


@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Evaluate a player's decision."""
    data = request.json
    difficulty = data.get('difficulty')
    scenario_id = data.get('scenario_id')
    chosen_action = data.get('action')

    # Get the scenario
    if difficulty == 'beginner':
        scenarios = get_beginner_scenarios()
    elif difficulty == 'intermediate':
        scenarios = get_intermediate_scenarios()
    else:
        return jsonify({'error': 'Invalid difficulty'}), 400

    if scenario_id >= len(scenarios):
        return jsonify({'error': 'Invalid scenario ID'}), 400

    scenario = scenarios[scenario_id]

    # Convert action string to Action enum
    from ..scenarios.scenario import Action
    action_map = {
        'fold': Action.FOLD,
        'check': Action.CHECK,
        'call': Action.CALL,
        'bet': Action.BET,
        'raise': Action.RAISE,
    }

    if chosen_action not in action_map:
        return jsonify({'error': 'Invalid action'}), 400

    action_enum = action_map[chosen_action]

    # Evaluate the decision
    evaluation = evaluator.evaluate_decision(scenario, action_enum)

    # Track stats in session
    if 'total_scenarios' not in session:
        session['total_scenarios'] = 0
        session['good_decisions'] = 0

    session['total_scenarios'] += 1
    if evaluation.grade.grade_value >= 4:  # Good or better
        session['good_decisions'] += 1

    return jsonify({
        'chosen_action': evaluation.chosen_action.value,
        'grade': evaluation.grade.label,
        'grade_value': evaluation.grade.grade_value,
        'best_action': evaluation.best_action.value,
        'explanation': evaluation.explanation,
        'stats': {
            'total': session['total_scenarios'],
            'good': session['good_decisions'],
            'accuracy': round(session['good_decisions'] / session['total_scenarios'] * 100, 1)
        }
    })


@app.route('/api/stats')
def get_stats():
    """Get user statistics."""
    return jsonify({
        'total': session.get('total_scenarios', 0),
        'good': session.get('good_decisions', 0),
        'accuracy': round(session.get('good_decisions', 0) / max(session.get('total_scenarios', 1), 1) * 100, 1)
    })


@app.route('/api/reset-stats', methods=['POST'])
def reset_stats():
    """Reset user statistics."""
    session['total_scenarios'] = 0
    session['good_decisions'] = 0
    session_id = session.get('session_id')
    if session_id and session_id in adaptive_difficulties:
        adaptive_difficulties[session_id].reset()
    return jsonify({'success': True})


@app.route('/api/generate-scenario')
def generate_scenario():
    """Generate a new random scenario."""
    difficulty = request.args.get('difficulty', 'beginner')

    # Generate scenario
    scenario = generator.generate(difficulty)

    # Convert to JSON
    scenario_data = {
        'id': -1,  # Generated scenarios have negative ID
        'name': scenario.name,
        'description': scenario.description,
        'position': scenario.hero_position.abbr,
        'position_full': scenario.hero_position.full_name,
        'cards': [str(c) for c in scenario.hero_cards],
        'cards_parseable': [c.rank.symbol + c.suit.name[0].lower() for c in scenario.hero_cards],
        'board': [str(c) for c in scenario.board_cards],
        'pot': scenario.pot_size,
        'current_bet': scenario.current_bet,
        'action_history': [
            {
                'position': action.position.abbr,
                'action': action.action.value,
                'amount': action.amount
            }
            for action in scenario.action_history
        ],
        'available_actions': [action.value for action in scenario.available_actions],
        'difficulty': scenario.difficulty,
    }

    # Store in session for evaluation
    if 'generated_scenario' not in session:
        session['generated_scenario'] = {}
    session['generated_scenario'] = scenario_data

    return jsonify(scenario_data)


@app.route('/api/adaptive-scenario')
def adaptive_scenario():
    """Get next scenario with adaptive difficulty."""
    # Get or create adaptive difficulty tracker for this session
    session_id = session.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(8)
        session['session_id'] = session_id

    if session_id not in adaptive_difficulties:
        adaptive_difficulties[session_id] = AdaptiveDifficulty()

    adaptive = adaptive_difficulties[session_id]
    difficulty = adaptive.get_current_difficulty()

    # Generate scenario at current difficulty
    scenario = generator.generate(difficulty)

    # Convert to JSON (same as above)
    scenario_data = {
        'id': -1,
        'name': scenario.name,
        'description': scenario.description,
        'position': scenario.hero_position.abbr,
        'position_full': scenario.hero_position.full_name,
        'cards': [str(c) for c in scenario.hero_cards],
        'cards_parseable': [c.rank.symbol + c.suit.name[0].lower() for c in scenario.hero_cards],  # e.g., "Ah", "Kd"
        'board': [str(c) for c in scenario.board_cards],
        'pot': scenario.pot_size,
        'current_bet': scenario.current_bet,
        'action_history': [
            {
                'position': action.position.abbr,
                'action': action.action.value,
                'amount': action.amount
            }
            for action in scenario.action_history
        ],
        'available_actions': [action.value for action in scenario.available_actions],
        'difficulty': difficulty,
        'adaptive_stats': adaptive.get_performance_summary(),
    }

    session['generated_scenario'] = scenario_data

    return jsonify(scenario_data)


@app.route('/api/evaluate-generated', methods=['POST'])
def evaluate_generated():
    """Evaluate a generated scenario."""
    data = request.json
    chosen_action = data.get('action')
    use_adaptive = data.get('adaptive', False)

    # Get the stored scenario
    scenario_data = session.get('generated_scenario')
    if not scenario_data:
        return jsonify({'error': 'No generated scenario found'}), 400

    # Reconstruct scenario object for evaluation
    from ..scenarios.scenario import Scenario, Action, PlayerAction, Street
    from ..core import Position, parse_cards

    # Map position abbreviation back to Position enum
    position_map = {p.abbr: p for p in Position}
    hero_position = position_map[scenario_data['position']]

    # Parse cards (use parseable format if available, fallback to display format)
    cards_to_parse = scenario_data.get('cards_parseable', scenario_data['cards'])
    hero_cards = parse_cards(' '.join(cards_to_parse))

    # Reconstruct action history
    action_map_str = {
        'fold': Action.FOLD,
        'check': Action.CHECK,
        'call': Action.CALL,
        'bet': Action.BET,
        'raise': Action.RAISE,
    }

    action_history = []
    for ah in scenario_data['action_history']:
        action_history.append(
            PlayerAction(
                position_map[ah['position']],
                action_map_str[ah['action']],
                ah.get('amount')
            )
        )

    scenario = Scenario(
        name=scenario_data['name'],
        description=scenario_data['description'],
        hero_position=hero_position,
        hero_cards=hero_cards,
        board_cards=[],
        street=Street.PREFLOP,
        pot_size=scenario_data['pot'],
        current_bet=scenario_data['current_bet'],
        action_history=action_history,
    )

    # Evaluate
    action_enum = action_map_str[chosen_action]
    evaluation = evaluator.evaluate_decision(scenario, action_enum)

    # Update adaptive difficulty if in adaptive mode
    if use_adaptive:
        session_id = session.get('session_id')
        if session_id and session_id in adaptive_difficulties:
            adaptive = adaptive_difficulties[session_id]
            adaptive.record_result(evaluation.grade.grade_value)

    # Track stats
    if 'total_scenarios' not in session:
        session['total_scenarios'] = 0
        session['good_decisions'] = 0

    session['total_scenarios'] += 1
    if evaluation.grade.grade_value >= 4:
        session['good_decisions'] += 1

    result = {
        'chosen_action': evaluation.chosen_action.value,
        'grade': evaluation.grade.label,
        'grade_value': evaluation.grade.grade_value,
        'best_action': evaluation.best_action.value,
        'explanation': evaluation.explanation,
        'stats': {
            'total': session['total_scenarios'],
            'good': session['good_decisions'],
            'accuracy': round(session['good_decisions'] / session['total_scenarios'] * 100, 1)
        }
    }

    # Add adaptive stats if applicable
    if use_adaptive:
        session_id = session.get('session_id')
        if session_id and session_id in adaptive_difficulties:
            result['adaptive_stats'] = adaptive_difficulties[session_id].get_performance_summary()

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
