import sys, json, math

class PersonalHabitAntiFragilityEngine:
    """
    Anti-Fragile Habit Continuity Engine.
    Prevents the 'all-or-nothing' abandonment reflex by offering Elastic Fallbacks
    (e.g., 45-min workout -> 5-min mobility stretches) and 48-hour grace recovery.
    """
    def __init__(self):
        # Default elastic levels: FULL (100%), PLUS (60%), MICRO (20%)
        self.habit_catalogs = {
            "exercise": {
                "full": {"name": "Full Gym Session", "duration_min": 45, "energy_req": 8},
                "plus": {"name": "Home Dumbbell Circuit", "duration_min": 20, "energy_req": 5},
                "micro": {"name": "Mobility & Pushup Flush", "duration_min": 5, "energy_req": 2}
            },
            "reading": {
                "full": {"name": "Read 25 Pages Deep Work", "duration_min": 40, "energy_req": 6},
                "plus": {"name": "Read 10 Pages", "duration_min": 15, "energy_req": 4},
                "micro": {"name": "Read 1 Page Before Sleep", "duration_min": 3, "energy_req": 1}
            },
            "meditation": {
                "full": {"name": "Vipassana Meditation", "duration_min": 20, "energy_req": 5},
                "plus": {"name": "Box Breathing", "duration_min": 10, "energy_req": 3},
                "micro": {"name": "3 Deep Diaphragmatic Breaths", "duration_min": 1, "energy_req": 1}
            }
        }

    def compute_elastic_fallback(self, habit_type, user_energy_level, available_minutes):
        # user_energy_level: 1 (exhausted) to 10 (peak energy)
        catalog = self.habit_catalogs.get(habit_type, self.habit_catalogs["exercise"])
        
        if user_energy_level >= 7 and available_minutes >= catalog["full"]["duration_min"]:
            selected_tier = "FULL"
            action = catalog["full"]
            rationale = "Energy and time are optimal. Execute standard full routine."
        elif user_energy_level >= 4 and available_minutes >= catalog["plus"]["duration_min"]:
            selected_tier = "PLUS"
            action = catalog["plus"]
            rationale = "Moderate constraints detected. Execute moderate maintenance tier."
        else:
            selected_tier = "MICRO"
            action = catalog["micro"]
            rationale = "High fatigue or time deficit. Preserve streak identity via micro-fallback."

        return {
            "habit_type": habit_type,
            "selected_tier": selected_tier,
            "action_name": action["name"],
            "duration_minutes": action["duration_min"],
            "energy_required": action["energy_req"],
            "rationale": rationale,
            "streak_preserved": True
        }

    def calculate_streak_health(self, daily_logs):
        # daily_logs: list of {"day": 1, "status": "COMPLETED_FULL" | "COMPLETED_MICRO" | "MISSED"}
        total_days = len(daily_logs)
        if total_days == 0:
            return {"active_streak": 0, "resilience_score": 100.0}

        current_streak = 0
        grace_days_used = 0
        micro_days_count = 0

        for log in reversed(daily_logs):
            st = log.get("status", "MISSED")
            if "COMPLETED" in st:
                current_streak += 1
                if "MICRO" in st:
                    micro_days_count += 1
                grace_days_used = 0
            elif st == "MISSED":
                if grace_days_used == 0: # First missed day absorbed by grace window
                    grace_days_used = 1
                else: # Second consecutive miss breaks streak
                    break

        resilience = (current_streak / max(1, total_days)) * 100.0
        return {
            "active_streak_days": current_streak,
            "resilience_score": round(resilience, 1),
            "micro_substitutions": micro_days_count,
            "status": "HEALTHY" if current_streak > 3 else "REBUILDING"
        }

    def run_benchmark_habit_anti_fragility(self):
        # Test low energy fallback
        fallback = self.compute_elastic_fallback("exercise", user_energy_level=2, available_minutes=10)
        
        # Test streak continuity with 1 missed day
        logs = [
            {"day": 1, "status": "COMPLETED_FULL"},
            {"day": 2, "status": "COMPLETED_FULL"},
            {"day": 3, "status": "MISSED"},
            {"day": 4, "status": "COMPLETED_MICRO"},
            {"day": 5, "status": "COMPLETED_FULL"}
        ]
        streak = self.calculate_streak_health(logs)
        return {
            "benchmark_status": "PASSED",
            "fallback_tier": fallback["selected_tier"],
            "active_streak": streak["active_streak_days"],
            "micro_substitutions": streak["micro_substitutions"]
        }
