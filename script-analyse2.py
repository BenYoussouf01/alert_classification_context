import json
from collections import Counter

INPUT_FILE = "Context-results_runs-linux.json"
OUTPUT_FILE = "Context-analysis_runs-linux1.json"

# Load all runs
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_results = json.load(f)

analysis = {}

print("\n📊 ANALYSIS REPORT\n")

for alert_id, runs in all_results.items():

    decisions = []
    description = None  # We will extract the description from output text

    for r in runs:
        if "output" not in r:
            continue

        line = r["output"]

        # ---- Extract alert_decision ----
        if "alert_decision:" in line:
            try:
                dec = line.split("alert_decision:")[1].split("|")[0].strip()
                decisions.append(dec)
            except:
                pass

        # ---- Extract alert_description (only once) ----
        if description is None and "alert_description:" in line:
            try:
                description = line.split("alert_description:")[1].split("|")[0].strip()
            except:
                description = "Unknown description"

    # If still no description found
    if description is None:
        description = "Unknown description"

    # Compute stats
    counter = Counter(decisions)
    total_runs = len(decisions)

    most_common_decision, freq = counter.most_common(1)[0]
    S_conf = freq / total_runs if total_runs else 0

    analysis[alert_id] = {
        "alert_description": description,
        "total_runs": total_runs,
        "decision_distribution": dict(counter),
        "most_common_decision": most_common_decision,
        "frequency": freq,
        "S_conf": round(S_conf, 4),
        "variation_count": total_runs - freq,
        "variation_rate": round((total_runs - freq) / total_runs, 4)
    }

    # ---- PRINT RESULT ----
    print(f"Alert {alert_id}")
    print(f"Description : {description}")
    print(f"Most common : {most_common_decision} ({freq}/{total_runs})")
    print(f"S_conf      : {S_conf:.4f}")
    print(f"Variations  : {total_runs - freq}")
    print(f"Distribution: {dict(counter)}\n")

# Save full analysis
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(analysis, f, indent=4)

print(f"📄 Full analysis saved to {OUTPUT_FILE}")
