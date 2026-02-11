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
with open("Alertes-wind.json") as f:
    alerts = json.load(f)

# with open("contexte.json") as f:
   #  context = json.load(f)

# Storage for all runs
all_results = {}

for index, alert in enumerate(alerts):
    alert_id = alert.get("id", f"alert_{index}")
    print(f"\n🔄 Processing alert {index+1}/{len(alerts)} — ID: {alert_id}")

    all_results[alert_id] = []

    # Build prompt
    base_message = (
        f"You are an experienced tier 1 SOC analyst. Review the SIEM alerts and decide which alerts are "
        f"interesting or not - interesting. An interesting alert indicates a potential incident that needs "
        f"to be investigated further. A non-interesting alert is either informational or a false positive. "
        f"Make this decision based on the details in the alert and respond with your decision. There is one "
        f"Wazuh alert in JSON format. Please review the alert and indicate whether it is 'interesting' "
        f"or 'not-interesting'. Your message should use the following format: alert_id: <ID> | alert_description: <short> | "
        f"alert_decision: <interesting|not-interesting> | reason: <brief>. \n\n"
        f"Alert: {alert}"
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
with open("essairuns-windowsvrai windows.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("\n🎉 DONE! All results saved to: essairuns-windows.json")