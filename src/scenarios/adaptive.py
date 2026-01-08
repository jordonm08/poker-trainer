"""
Adaptive difficulty system - adjusts based on player performance.
"""
from typing import List
from collections import deque


class AdaptiveDifficulty:
    """
    Manages difficulty progression based on performance.

    Tracks recent performance and adjusts difficulty level accordingly.
    """

    def __init__(self, window_size: int = 10):
        """
        Args:
            window_size: Number of recent scenarios to consider for difficulty adjustment
        """
        self.window_size = window_size
        self.recent_scores = deque(maxlen=window_size)
        self.current_difficulty = 'beginner'
        self.total_scenarios = 0

    def record_result(self, grade_value: int):
        """
        Record the result of a scenario.

        Args:
            grade_value: Grade value (1-5, where 5 is Excellent)
        """
        self.recent_scores.append(grade_value)
        self.total_scenarios += 1

        # Update difficulty if we have enough data
        if len(self.recent_scores) >= self.window_size:
            self._update_difficulty()

    def _update_difficulty(self):
        """Update difficulty based on recent performance."""
        if len(self.recent_scores) == 0:
            return

        avg_score = sum(self.recent_scores) / len(self.recent_scores)

        # Current difficulty thresholds
        if self.current_difficulty == 'beginner':
            # Move to intermediate if averaging 4+ (Good or better)
            if avg_score >= 4.0:
                self.current_difficulty = 'intermediate'
                print(f"\n🎉 Great job! Moving to INTERMEDIATE difficulty.\n")

        elif self.current_difficulty == 'intermediate':
            # Move to advanced if averaging 4+
            if avg_score >= 4.2:
                self.current_difficulty = 'advanced'
                print(f"\n🎉 Excellent! Moving to ADVANCED difficulty.\n")
            # Drop back to beginner if struggling
            elif avg_score < 3.0:
                self.current_difficulty = 'beginner'
                print(f"\n💡 Dropping back to BEGINNER to build fundamentals.\n")

        elif self.current_difficulty == 'advanced':
            # Drop to intermediate if struggling
            if avg_score < 3.0:
                self.current_difficulty = 'intermediate'
                print(f"\n💡 Dropping to INTERMEDIATE difficulty.\n")

    def get_current_difficulty(self) -> str:
        """Get the current difficulty level."""
        return self.current_difficulty

    def get_performance_summary(self) -> dict:
        """Get performance statistics."""
        if len(self.recent_scores) == 0:
            return {
                'avg_score': 0.0,
                'difficulty': self.current_difficulty,
                'total_scenarios': self.total_scenarios,
                'window_size': len(self.recent_scores),
            }

        return {
            'avg_score': round(sum(self.recent_scores) / len(self.recent_scores), 2),
            'difficulty': self.current_difficulty,
            'total_scenarios': self.total_scenarios,
            'window_size': len(self.recent_scores),
            'recent_scores': list(self.recent_scores),
        }

    def reset(self):
        """Reset the adaptive difficulty system."""
        self.recent_scores.clear()
        self.current_difficulty = 'beginner'
        self.total_scenarios = 0
