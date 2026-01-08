"""
Web interface for poker trainer using Flask.
"""
from flask import Flask, render_template, request, jsonify, session
import os
import secrets

from ..scenarios.library import get_beginner_scenarios, get_intermediate_scenarios
from ..grading.evaluator import DecisionEvaluator

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

evaluator = DecisionEvaluator()


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
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
