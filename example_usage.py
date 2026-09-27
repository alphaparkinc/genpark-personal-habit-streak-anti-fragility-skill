import sys, json
from client import PersonalHabitAntiFragilityEngine

def main():
    print("Testing PersonalHabitAntiFragilityEngine...")
    engine = PersonalHabitAntiFragilityEngine()
    res = engine.run_benchmark_habit_anti_fragility()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["fallback_tier"] == "MICRO"
    assert res["active_streak"] >= 3
    print("All Personal Habit Anti-Fragility tests passed successfully!")

if __name__ == "__main__":
    main()
