"""Quick demo to show how scenarios display action history."""
from src.scenarios.library import get_beginner_scenarios

scenarios = get_beginner_scenarios()

print("=" * 70)
print("DEMO: How scenarios show previous action".center(70))
print("=" * 70)

for i, scenario in enumerate(scenarios, 1):
    print(f"\n{'='*70}")
    print(f"SCENARIO {i}: {scenario.name}")
    print('='*70)
    print(scenario.get_description_text())
    print()

print("\n" + "="*70)
print("Notice how scenarios now clearly show what happened before you!")
print("="*70)
