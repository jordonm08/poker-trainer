"""
Simple command-line interface for poker trainer.
"""
import sys
from typing import Optional

from ..scenarios.scenario import Scenario, Action
from ..scenarios.library import get_beginner_scenarios, get_intermediate_scenarios
from ..grading.evaluator import DecisionEvaluator, Grade


class PokerTrainerCLI:
    """Command-line interface for poker training."""

    def __init__(self):
        self.evaluator = DecisionEvaluator()
        self.current_scenario: Optional[Scenario] = None
        self.score = 0
        self.total_scenarios = 0

    def run(self):
        """Run the main application loop."""
        self.show_welcome()

        while True:
            choice = self.show_main_menu()

            if choice == "1":
                self.practice_mode("beginner")
            elif choice == "2":
                self.practice_mode("intermediate")
            elif choice == "3":
                self.show_stats()
            elif choice == "4":
                print("\nThanks for practicing! Good luck at the tables.")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_welcome(self):
        """Display welcome message."""
        print("=" * 60)
        print("POKER TRAINER".center(60))
        print("=" * 60)
        print("\nImprove your poker skills with scenario-based training!")
        print("Make decisions and get instant feedback based on poker theory.")
        print()

    def show_main_menu(self) -> str:
        """Show main menu and get user choice."""
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Practice (Beginner)")
        print("2. Practice (Intermediate)")
        print("3. View Stats")
        print("4. Quit")
        print()
        return input("Choose an option (1-4): ").strip()

    def practice_mode(self, difficulty: str):
        """Run practice mode with scenarios."""
        if difficulty == "beginner":
            scenarios = get_beginner_scenarios()
        elif difficulty == "intermediate":
            scenarios = get_intermediate_scenarios()
        else:
            scenarios = get_beginner_scenarios()

        print(f"\n{'='*60}")
        print(f"{difficulty.upper()} PRACTICE MODE".center(60))
        print(f"{'='*60}")
        print(f"You have {len(scenarios)} scenarios to complete.\n")

        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'='*60}")
            print(f"SCENARIO {i}/{len(scenarios)}: {scenario.name}")
            print(f"{'='*60}")
            self.present_scenario(scenario)

        print(f"\n{'='*60}")
        print(f"Practice complete! You finished all {len(scenarios)} scenarios.")
        print(f"{'='*60}")

    def present_scenario(self, scenario: Scenario):
        """Present a scenario and get user decision."""
        self.current_scenario = scenario

        # Show scenario details
        print(f"\n{scenario.get_description_text()}")

        # Show available actions
        print("\nWhat do you do?")
        actions = scenario.available_actions
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action.value.capitalize()}")

        # Get user choice
        while True:
            try:
                choice = input("\nYour choice (number): ").strip()
                choice_idx = int(choice) - 1

                if 0 <= choice_idx < len(actions):
                    chosen_action = actions[choice_idx]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(actions)}")
            except ValueError:
                print("Please enter a valid number")

        # Evaluate decision
        evaluation = self.evaluator.evaluate_decision(scenario, chosen_action)

        # Show results
        self.show_evaluation(evaluation)

        # Update stats
        self.total_scenarios += 1
        if evaluation.grade.grade_value >= Grade.GOOD.grade_value:
            self.score += 1

    def show_evaluation(self, evaluation):
        """Display evaluation results."""
        print("\n" + "=" * 60)
        print("EVALUATION")
        print("=" * 60)

        # Show grade with visual indicator
        grade_symbols = {
            Grade.EXCELLENT: "★★★★★",
            Grade.GOOD: "★★★★☆",
            Grade.INACCURATE: "★★★☆☆",
            Grade.MISTAKE: "★★☆☆☆",
            Grade.BLUNDER: "★☆☆☆☆",
        }

        print(f"\nYour move: {evaluation.chosen_action.value.upper()}")
        print(f"Grade: {evaluation.grade.label} {grade_symbols[evaluation.grade]}")

        if evaluation.chosen_action != evaluation.best_action:
            print(f"Best move: {evaluation.best_action.value.upper()}")

        print(f"\n{evaluation.explanation}")
        print("=" * 60)

        input("\nPress Enter to continue...")

    def show_stats(self):
        """Display user statistics."""
        print("\n" + "=" * 60)
        print("YOUR STATISTICS")
        print("=" * 60)

        if self.total_scenarios == 0:
            print("\nNo scenarios completed yet. Start practicing to see stats!")
        else:
            accuracy = (self.score / self.total_scenarios) * 100
            print(f"\nScenarios completed: {self.total_scenarios}")
            print(f"Good+ decisions: {self.score}")
            print(f"Accuracy: {accuracy:.1f}%")

        print("=" * 60)


def main():
    """Main entry point."""
    app = PokerTrainerCLI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Thanks for practicing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
