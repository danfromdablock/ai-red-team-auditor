"""The website: a form to paste a system prompt, and a page that shows the report."""
import sys
from datetime import datetime, timezone

from flask import Flask, render_template, request

from auditor import PERSONAS, active_provider, model_name, run_audit

app = Flask(__name__)

# Lower number = worse. Used to pick the overall risk.
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Unknown": 4}


@app.route("/")
def index():
    return render_template("index.html", personas=PERSONAS)


@app.route("/audit", methods=["POST"])
def audit():
    system_prompt = request.form.get("system_prompt", "").strip()
    persona_key = request.form.get("persona", "job_applicant")
    custom_persona = request.form.get("custom_persona", "").strip()

    if not system_prompt:
        return render_template("index.html", personas=PERSONAS, error="Please paste a system prompt to audit.")

    results = run_audit(system_prompt, persona_key, custom_persona)
    overall = min((r.get("severity", "Unknown") for r in results), key=lambda s: SEVERITY_ORDER.get(s, 4))
    persona = custom_persona or PERSONAS.get(persona_key, persona_key)

    # Everything the "Download JSON" button saves
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": model_name(),
        "persona": persona,
        "system_prompt": system_prompt,
        "overall_severity": overall,
        "results": results,
    }
    return render_template("report.html", report=report)


if __name__ == "__main__":
    if not active_provider():
        print("No API key found. Open your .env file and paste a GEMINI_API_KEY (or GROQ_API_KEY).")
        sys.exit(1)
    print(f"Using {active_provider()} ({model_name()})")
    app.run(debug=True, port=5000)
