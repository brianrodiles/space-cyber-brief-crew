# Space Cyber Brief Crew

AI-powered multi-agent cyber threat intelligence briefing pipeline built with CrewAI.

This project explores how autonomous AI agents can monitor open-source intelligence (OSINT) feeds and generate structured cyber threat briefs related to space systems, satellite infrastructure, and critical technologies.

---

## Problem

Cyber threats targeting space infrastructure are increasing. Security teams must monitor multiple intelligence feeds, analyze signals, and produce actionable reports quickly.

Manual workflows are slow and difficult to scale.

This project experiments with **AI agent orchestration** to automate threat intelligence collection and briefing.

---

## Architecture

The system uses multiple AI agents:

1. **Collector Agent**
   - Pulls OSINT feeds
   - Collects cyber threat signals

2. **Analysis Agent**
   - Evaluates relevance
   - Identifies patterns or emerging threats

3. **Briefing Agent**
   - Generates structured intelligence briefs
   - Summarizes findings for analysts

---

## Example Output

Daily intelligence brief format:

Threat Area: Satellite communications security

Summary:
New vulnerabilities reported affecting ground station software used in multiple satellite networks.

Potential Impact:
Unauthorized command injection and signal disruption.

Recommended Monitoring:
CISA KEV database  
Satellite network telemetry anomalies  
Vendor patch advisories

---

## Technology Stack

- Python
- CrewAI
- OpenAI APIs
- OSINT feeds
- Multi-agent orchestration

---

## Run it on Windows (PowerShell)

Run these commands from the project directory, `Documents\space-cyber-brief-crew`. Python 3.10 or newer is recommended.

### 1. Create the environment and install packages

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt crewai
```

If PowerShell blocks virtual-environment activation, allow it for this terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Add your model API key

The CrewAI command requires a model-provider API key and internet access to that provider. Create a local `.env` from the example and edit it:

```powershell
Copy-Item .env.example .env
notepad .env
```

Put your key after `OPENAI_API_KEY=` and save. Keep `.env` private; do not commit it. The current workflow checks for either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.

### 3. Add sources and generate a brief

Place one or more source documents ending in `.txt` or `.md` in `sources/`. Then run:

```powershell
python main.py
Get-Content .\output\daily_brief.md
```

The command runs the sequential Collector → Analyst → Writer workflow and writes `output/daily_brief.md`. The sample source files are already in `sources/`, so they can be used for an initial run. Check claims against the source documents before using or distributing a brief.

### 4. (Optional) Start the signal API

Open a second PowerShell window, change to the project directory, and activate the environment as above. Then run:

```powershell
python -m uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the endpoints interactively. `GET /api/signals` reads the configured CISA RSS feeds, so it needs internet access. To submit a draft request from PowerShell:

```powershell
$body = @{
  source = 'Example advisory'
  title = 'Satellite ground station software vulnerability'
  summary = 'An advisory reports a vulnerability affecting a network-connected ground station component.'
  link = 'https://example.com/advisory'
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/api/generate-brief' -ContentType 'application/json' -Body $body
```

This API is separate from the CrewAI brief workflow. It uses keyword scoring and fixed rules to produce analyst-review drafts; it does not call an LLM. Treat the results as triage aids, not validated intelligence.

## Repository layout

```text
config/       CrewAI agent and task prompts
output/       Generated brief output
sources/      Approved local text/Markdown source corpus
tools/        File reader tool used by the Collector
api.py        Separate FastAPI RSS triage and draft endpoints
crew.py       Three-stage sequential agent workflow
guardrails.py Shared operational prompt rules
main.py       Local workflow entry point
```

## Future Work

Planned enhancements:

- Integration with CISA KEV feed
- Satellite vulnerability tracking
- Automated weekly threat intelligence reports
- Visualization dashboard

---

## Authors

Khadija Taki  
MSISPM – Carnegie Mellon University  
Cybersecurity | AI | Space Systems Security

Brian G. Rodiles Delgado  
Cybersecurity Management MBA – University of West Florida    
Industrial Control Systems (ICS) | Operational Technology (OT) | Agentic Infrastructure/Evaluations