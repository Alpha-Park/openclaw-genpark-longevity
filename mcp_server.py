import sys, json
from client import LongevityBiomarkerEstimatorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    estimator = LongevityBiomarkerEstimatorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "openclaw-genpark-longevity"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    c_age = req.get("chronological_age", 40.0)
    bio = req.get("biomarkers", {})
    res = estimator.calculate_biological_age(c_age, bio)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
