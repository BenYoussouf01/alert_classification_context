import json
import os
import time
from together import Together

# --- CONFIGURATION ---
RUNS = 100   # Mets 5 pour tester, puis 100 pour final
MODEL_NAME = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

API_KEY = os.environ.get("TOGETHER_API_KEY")
if not API_KEY:
    print("❌ ERROR: TOGETHER_API_KEY not set.")
    raise SystemExit(1)

client = Together(api_key=API_KEY)

# Load alerts and context
with open("alert-linux.json") as f:
    alerts = json.load(f)

with open("contexte.json") as f:
    context = json.load(f)

# Storage for all runs
all_results = {}

for index, alert in enumerate(alerts):
    alert_id = alert.get("id", f"alert_{index}")
    print(f"\n🔄 Processing alert {index+1}/{len(alerts)} — ID: {alert_id}")

    all_results[alert_id] = []

    # Build prompt
    base_message = (
        f"You are an experienced Tier 1 SOC analyst. Review the following SIEM alert and decide if it is "
        f"'interesting' or 'not-interesting'. An interesting alert indicates a potential incident requiring "
        f"investigation, while a non-interesting alert is informational or benign.\n\n"
        f"Use the BUSINESS CONTEXT as a guide to understand the organization's normal behavior "
        f"(its users, groups, assets, business hours, and networks). Analyze the alert in this context and "
        f"make your own judgment.\n\n"
        f"In your explanation, clearly mention which factors from the context influenced your decision — "
        f"for example, user group, account type, business hours, host role, network location, or other details.\n\n"
        f"Respond strictly using this format:\n"
        f"alert_id: <ID> | alert_description: <short> | alert_decision: <interesting|not-interesting> | "
        f"reason: <brief explanation mentioning contextual factors>\n\n"
        f"ALERT:\n{json.dumps(alert, ensure_ascii=False)}\n\n"
        f"BUSINESS CONTEXT:\n{json.dumps(context, ensure_ascii=False)}"
    )

    for run in range(RUNS):
        print(f"  → Run {run+1}/{RUNS}", end="\r")

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": base_message}]
            )
            output = response.choices[0].message.content.strip()

            all_results[alert_id].append({
                "run": run + 1,
                "output": output
            })

            # Avoid rate limits
            time.sleep(0.4)

        except Exception as e:
            print(f"\n❌ ERROR on run {run+1}: {e}")
            all_results[alert_id].append({
                "run": run + 1,
                "error": str(e)
            })
            time.sleep(1)

# Save results
with open("Context-results_runs-linux.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("\n🎉 DONE! All results saved to: Context-results_runs-linux.json")