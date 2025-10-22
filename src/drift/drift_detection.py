import json

with open("reports/drift_summary.json") as f:
    drift = json.load(f)

if drift["data_drift_detected"] or drift["concept_drift_detected"]:
    open("trigger_retrain.flag", "w").write("1")
else:
    print("No drift detected; skipping retrain.")
