import sys, json
from client import PersonalHabitAntiFragilityEngine

def main():
    engine = PersonalHabitAntiFragilityEngine()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(engine.run_benchmark_habit_anti_fragility(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "compute_elastic_fallback", "description": "Select habit micro-tier under low energy/time constraints."},
                        {"name": "calculate_streak_health", "description": "Calculate streak length with elastic grace window."},
                        {"name": "run_benchmark_habit_anti_fragility", "description": "Run habit resilience benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "compute_elastic_fallback":
                    out = engine.compute_elastic_fallback(args.get("habit_type", "exercise"), args.get("user_energy_level", 5), args.get("available_minutes", 15))
                elif tname == "calculate_streak_health":
                    out = engine.calculate_streak_health(args.get("daily_logs", []))
                elif tname == "run_benchmark_habit_anti_fragility":
                    out = engine.run_benchmark_habit_anti_fragility()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
