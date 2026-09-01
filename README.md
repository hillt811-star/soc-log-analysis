# SOC Log Analysis — Authentication Triage (Showcase)

One-line summary:
Parse and analyze authentication logs to detect suspicious login patterns and demonstrate SOC triage and investigation.

Objective
- Show foundational skills in log parsing, SQL/Pandas-based analysis, basic detection logic, and an investigative narrative suitable for interviews.

Tech stack
- Python 3.9+, pandas, CSV/SQLite (optional), Jupyter Notebook (optional)

What I built
- src/parse_logs.py — parser and simple detection script that summarizes failed logins and flags suspicious IPs
- data/auth_logs_sample.csv — sanitized synthetic data for demo
- notebooks/analysis_outline.md — suggested Jupyter walk-through with visualizations and queries

How to run (local)
1. Clone repo
2. Create virtualenv:
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
3. Install:
   pip install -r requirements.txt
4. Run the parser:
   python src/parse_logs.py data/auth_logs_sample.csv
5. (Optional) Open notebooks/analysis_outline.md to build the notebook or convert it to analysis.ipynb

Detection summary (example)
- The parser prints top IPs by failed attempts and highlights IPs exceeding a configurable threshold (default: 10).
- Use the output to drive triage: check user accounts targeted, correlate timestamps, and enrich with geo/IP intel.

Sample Splunk search (concept)
index=auth sourcetype=linux_secure action=failed | stats count by src_ip, user | where count > 10

What to include in your portfolio entry
- README top-level TL;DR and 1–2 screenshots or a short (30–90s) demo GIF showing the script or notebook output
- A short "What I learned" section describing the analysis steps, challenges, and next improvements
- Links to your LinkedIn/resume and contact info

Next steps you can do (prioritized)
1. Convert notebooks/analysis_outline.md into notebooks/analysis.ipynb and create charts (failed attempts over time, top users, heatmap).
2. Add a short demo GIF (record running the notebook/script).
3. Replace sample CSV with a slightly larger synthetic dataset (500–2,000 rows) and include sanity checks for privacy.
4. Add a Splunk or Sigma rule example and tuning notes in docs/.
5. Push to GitHub and add this repo to your GitHub profile README as a portfolio item.

If you want, I can push these files into a new GitHub repository named soc-log-analysis under your account. I can also run the notebook and add demo images if you prefer.
