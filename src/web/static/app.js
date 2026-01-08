let currentDifficulty = null;
let scenarios = [];
let currentScenarioIndex = 0;

// Position explanations for beginners
function getPositionHelp(positionAbbr) {
    const explanations = {
        'UTG': 'First to act - tightest range (play strong hands only)',
        'MP': 'Middle Position - moderate range',
        'CO': 'Cutoff (one before button) - wider range, good position',
        'BTN': 'Button (dealer) - best position, widest range, act last',
        'SB': 'Small Blind - bad position (act first post-flop)',
        'BB': 'Big Blind - last to act pre-flop, then first post-flop'
    };
    return explanations[positionAbbr] || '';
}

// Load stats on page load
loadStats();

function loadStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('total').textContent = data.total;
            document.getElementById('accuracy').textContent = data.accuracy + '%';
        });
}

function startPractice(difficulty) {
    currentDifficulty = difficulty;
    currentScenarioIndex = 0;

    fetch(`/api/scenarios/${difficulty}`)
        .then(res => res.json())
        .then(data => {
            scenarios = data;
            document.getElementById('menu').classList.add('hidden');
            showScenario(0);
        });
}

function showScenario(index) {
    if (index >= scenarios.length) {
        showComplete();
        return;
    }

    const scenario = scenarios[index];
    currentScenarioIndex = index;

    // Show scenario container
    document.getElementById('scenario-container').classList.remove('hidden');
    document.getElementById('result-container').classList.add('hidden');

    // Update header
    document.getElementById('scenario-title').textContent = scenario.name;
    document.getElementById('scenario-progress').textContent =
        `Scenario ${index + 1} of ${scenarios.length}`;

    // Update table info
    document.getElementById('position').textContent = scenario.position_full;

    // Add position explanation
    const positionHelp = getPositionHelp(scenario.position);
    document.getElementById('position-help').textContent = positionHelp;

    document.getElementById('pot').textContent = scenario.pot + ' BB';

    if (scenario.current_bet > 0) {
        document.getElementById('bet-row').style.display = 'flex';
        document.getElementById('bet-to-call').textContent = scenario.current_bet + ' BB';
    } else {
        document.getElementById('bet-row').style.display = 'none';
    }

    // Show cards
    const heroCards = document.getElementById('hero-cards');
    heroCards.innerHTML = '';
    scenario.cards.forEach(card => {
        const cardEl = document.createElement('div');
        cardEl.className = 'card';
        cardEl.textContent = card;
        heroCards.appendChild(cardEl);
    });

    // Show board if exists
    if (scenario.board && scenario.board.length > 0) {
        document.getElementById('board-section').style.display = 'block';
        const boardCards = document.getElementById('board-cards');
        boardCards.innerHTML = '';
        scenario.board.forEach(card => {
            const cardEl = document.createElement('div');
            cardEl.className = 'card';
            cardEl.textContent = card;
            boardCards.appendChild(cardEl);
        });
    } else {
        document.getElementById('board-section').style.display = 'none';
    }

    // Show action history
    const actionList = document.getElementById('action-list');
    actionList.innerHTML = '';

    if (scenario.action_history && scenario.action_history.length > 0) {
        scenario.action_history.forEach(action => {
            const actionEl = document.createElement('div');
            actionEl.className = 'action-item';
            let text = `${action.position} ${action.action}`;
            if (action.amount) {
                text += ` ${action.amount}BB`;
            }
            actionEl.textContent = text;
            actionList.appendChild(actionEl);
        });
    } else {
        const actionEl = document.createElement('div');
        actionEl.className = 'action-item';
        actionEl.textContent = '(You are first to act)';
        actionEl.style.fontStyle = 'italic';
        actionList.appendChild(actionEl);
    }

    // Show action buttons
    const actionButtons = document.getElementById('action-buttons');
    actionButtons.innerHTML = '';
    scenario.available_actions.forEach(action => {
        const btn = document.createElement('button');
        btn.className = 'action-btn';
        btn.textContent = action.charAt(0).toUpperCase() + action.slice(1);
        btn.onclick = () => makeDecision(action);
        actionButtons.appendChild(btn);
    });
}

function makeDecision(action) {
    fetch('/api/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            difficulty: currentDifficulty,
            scenario_id: currentScenarioIndex,
            action: action
        })
    })
    .then(res => res.json())
    .then(result => {
        showResult(result);
        loadStats();
    });
}

function showResult(result) {
    // Hide scenario, show result
    document.getElementById('scenario-container').classList.add('hidden');
    document.getElementById('result-container').classList.remove('hidden');

    // Show your action
    document.getElementById('your-action').textContent = result.chosen_action.toUpperCase();

    // Show grade
    const gradeEl = document.getElementById('grade');
    gradeEl.textContent = result.grade;
    gradeEl.className = 'grade ' + result.grade.toLowerCase();

    // Show stars
    const starsEl = document.getElementById('stars');
    const starCount = result.grade_value;
    const maxStars = 5;
    starsEl.textContent = '★'.repeat(starCount) + '☆'.repeat(maxStars - starCount);

    // Show best action if different
    if (result.chosen_action !== result.best_action) {
        document.getElementById('best-action-label').style.display = 'block';
        document.getElementById('best-action').style.display = 'block';
        document.getElementById('best-action').textContent = result.best_action.toUpperCase();
    } else {
        document.getElementById('best-action-label').style.display = 'none';
        document.getElementById('best-action').style.display = 'none';
    }

    // Show explanation
    document.getElementById('explanation').textContent = result.explanation;
}

function nextScenario() {
    showScenario(currentScenarioIndex + 1);
}

function showComplete() {
    document.getElementById('scenario-container').classList.add('hidden');
    document.getElementById('result-container').classList.add('hidden');
    document.getElementById('complete-container').classList.remove('hidden');

    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('final-total').textContent = data.total;
            document.getElementById('final-accuracy').textContent = data.accuracy + '%';
        });
}
