import json
import time
import requests

# --- CONFIGURATION ---
RUNS = 100
MODEL_NAME = "llama3.1:8b"   # mettre la version ollama

# Load alerts and context
with open("alert-linux.json", encoding="utf-8") as f:
    alerts = json.load(f)

with open("contexte.json", encoding="utf-8") as f:
    context = json.load(f)

# Storage for all runs
all_results = {}

for index, alert in enumerate(alerts):
    alert_id = alert.get("id", f"alert_{index}")
    print(f"\nProcessing alert {index+1}/{len(alerts)} - ID: {alert_id}")

    all_results[alert_id] = []

    # Build prompt
    base_message = (
        f"You are an experienced Tier 1 SOC analyst. Review the following SIEM alert and decide if it is "
        f"'interesting' or 'not-interesting'. An interesting alert indicates a potential incident requiring "
        f"investigation, while a non-interesting alert is informational or benign.\n\n"
        f"Use the BUSINESS CONTEXT as a guide to understand the organization's normal behavior "
        f"(its users, groups, assets, business hours, and networks). Analyze the alert in this context and "
        f"make your own judgment.\n\n"
        f"In your explanation, clearly mention which factors from the context influenced your decision - "
        f"for example, user group, account type, business hours, host role, network location, or other details.\n\n"
        f"Respond strictly using this format:\n"
        f"alert_id: <ID> | alert_description: <short> | alert_decision: <interesting|not-interesting> | "
        f"reason: <brief explanation mentioning contextual factors>\n\n"
        f"ALERT:\n{json.dumps(alert, ensure_ascii=False)}\n\n"
        f"BUSINESS CONTEXT:\n{json.dumps(context, ensure_ascii=False)}"
    )

    for run in range(RUNS):
        print(f"  -> Run {run+1}/{RUNS}", end="\r")

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": base_message}
                    ],
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()

            output = data["message"]["content"].strip()

            all_results[alert_id].append({
                "run": run + 1,
                "output": output
            })

            time.sleep(0.2)

        except Exception as e:
            print(f"\nERROR on run {run+1}: {e}")
            all_results[alert_id].append({
                "run": run + 1,
                "error": str(e)
            })
            time.sleep(1)

with open("Context-results-runs-ollama.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("\nDONE! All results saved to: Context-results-runs-ollama.json")
