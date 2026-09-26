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
Cybersecurity Management MBA - University of West Florida
Industrial Control Systems (ICS) | Operational Technology (OT) | Agentic Infrastructure/Evaluations