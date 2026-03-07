"""
Setup script for Space-Cyber Brief Crew v1
Run this once from inside the space-cyber-brief-crew folder:
    python setup.py
It will create all project files automatically.
"""

import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {path}")

print("Setting up Space-Cyber Brief Crew v1...")
print()

# ── main.py ──────────────────────────────────────────────
write_file("main.py", r'''import os
import sys
from datetime import datetime
from dotenv import load_dotenv

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: No API key found.")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file.")
        sys.exit(1)

    if not os.path.isdir("sources"):
        print("ERROR: sources/ directory not found.")
        sys.exit(1)

    source_files = [
        f for f in os.listdir("sources")
        if f.endswith((".txt", ".md")) and not f.startswith(".")
    ]
    if not source_files:
        print("ERROR: No source documents found in sources/.")
        sys.exit(1)

    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("  SPACE-CYBER BRIEF CREW v1")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Sources: {len(source_files)} document(s)")
    print("=" * 60)
    print()

    from crew import build_crew
    crew = build_crew()
    result = crew.kickoff()

    print()
    print("=" * 60)
    print("  CREW RUN COMPLETE")
    print("  Output: output/daily_brief.md")
    print("=" * 60)
    return result

if __name__ == "__main__":
    main()
''')

# ── crew.py ──────────────────────────────────────────────
write_file("crew.py", r'''import yaml
from crewai import Agent, Task, Crew, Process
from tools.file_reader import FileReaderTool
from guardrails import get_guardrail_prompt

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_crew():
    agent_configs = load_yaml("config/agents.yaml")
    task_configs = load_yaml("config/tasks.yaml")
    guardrails = get_guardrail_prompt()

    file_reader = FileReaderTool()

    collector = Agent(
        role=agent_configs["collector"]["role"],
        goal=agent_configs["collector"]["goal"],
        backstory=agent_configs["collector"]["backstory"] + "\n\n" + guardrails,
        verbose=True,
        allow_delegation=False,
        tools=[file_reader],
    )

    analyst = Agent(
        role=agent_configs["analyst"]["role"],
        goal=agent_configs["analyst"]["goal"],
        backstory=agent_configs["analyst"]["backstory"] + "\n\n" + guardrails,
        verbose=True,
        allow_delegation=False,
        tools=[],
    )

    writer = Agent(
        role=agent_configs["writer"]["role"],
        goal=agent_configs["writer"]["goal"],
        backstory=agent_configs["writer"]["backstory"] + "\n\n" + guardrails,
        verbose=True,
        allow_delegation=False,
        tools=[],
    )

    collect_task = Task(
        description=task_configs["collect_threats"]["description"],
        expected_output=task_configs["collect_threats"]["expected_output"],
        agent=collector,
    )

    analyze_task = Task(
        description=task_configs["analyze_threats"]["description"],
        expected_output=task_configs["analyze_threats"]["expected_output"],
        agent=analyst,
        context=[collect_task],
    )

    write_task = Task(
        description=task_configs["write_brief"]["description"],
        expected_output=task_configs["write_brief"]["expected_output"],
        agent=writer,
        context=[analyze_task],
        output_file="output/daily_brief.md",
    )

    crew = Crew(
        agents=[collector, analyst, writer],
        tasks=[collect_task, analyze_task, write_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew
''')

# ── guardrails.py ────────────────────────────────────────
write_file("guardrails.py", r'''OPERATIONAL_RULES = """
OPERATIONAL GUARDRAILS - ALL AGENTS MUST FOLLOW:
1. READ-ONLY SOURCES: Only read files from the approved sources/ directory.
2. NO CODE EXECUTION: Do not execute shell commands or scripts.
3. NO NETWORK ACCESS: Do not fetch URLs or call APIs.
4. NO MODIFICATION OF SOURCES: Never modify or delete source files.
5. OUTPUT ONLY TO APPROVED DIRECTORY: All output goes to output/ only.
6. SOURCE ATTRIBUTION: Every claim must reference a source document.
7. UNCERTAINTY LABELING: Flag uncertain conclusions explicitly.
8. NO FABRICATION: Do not invent facts. If info is missing, say so.
9. CLASSIFICATION: All output marked UNCLASSIFIED // FOR EDUCATIONAL USE.
10. SCOPE: Process cybersecurity threat intelligence only.
"""

def get_guardrail_prompt():
    return OPERATIONAL_RULES
''')

# ── tools/__init__.py ────────────────────────────────────
write_file("tools/__init__.py", r'''from tools.file_reader import FileReaderTool
__all__ = ["FileReaderTool"]
''')

# ── tools/file_reader.py ────────────────────────────────
write_file("tools/file_reader.py", r'''import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class FileReaderInput(BaseModel):
    directory: str = Field(default="sources", description="Path to source directory.")


class FileReaderTool(BaseTool):
    name: str = "Source Document Reader"
    description: str = "Reads all .txt and .md files from a directory and returns their contents."
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, directory: str = "sources") -> str:
        supported = (".txt", ".md")
        results = []
        if not os.path.isdir(directory):
            return f"Error: Directory '{directory}' not found."
        source_files = sorted([
            f for f in os.listdir(directory)
            if f.endswith(supported) and not f.startswith(".")
        ])
        if not source_files:
            return f"No source documents found in '{directory}'."
        for filename in source_files:
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                results.append(
                    f"=== SOURCE: {filename} ===\n{content}\n=== END: {filename} ===\n"
                )
            except Exception as e:
                results.append(
                    f"=== SOURCE: {filename} ===\nError: {e}\n=== END: {filename} ===\n"
                )
        return f"Found {len(source_files)} source document(s):\n\n" + "\n".join(results)
''')

# ── config/agents.yaml ──────────────────────────────────
write_file("config/agents.yaml", r'''collector:
  role: Cyber Threat Intelligence Collector
  goal: >
    Read all documents in the approved sources directory and extract
    a structured inventory of threat-relevant facts including titles,
    dates, affected systems, source names, and short summaries.
    Do NOT fabricate information.
  backstory: >
    You are a disciplined intelligence collector with experience in
    federal cybersecurity operations. You process raw advisories and
    reports from trusted sources. You never speculate beyond what the
    source material states.

analyst:
  role: Cyber Threat Analyst
  goal: >
    Take the collector output and perform threat analysis. For each
    item determine threat type, affected technology, severity
    (Critical/High/Medium/Low), and MITRE ATT&CK or ATLAS mappings.
    Flag uncertain mappings.
  backstory: >
    You are a senior threat analyst specializing in space systems
    security, critical infrastructure, and adversarial AI. You have
    deep familiarity with MITRE ATT&CK and ATLAS frameworks. You
    prioritize accuracy and label uncertain assessments.

writer:
  role: Intelligence Brief Writer
  goal: >
    Take the analyst assessments and produce a clear daily threat
    brief in markdown format with date, executive summary, per-item
    sections, and closing notes.
  backstory: >
    You are a communications specialist who writes intelligence
    products for senior leadership. Your briefs are known for
    clarity, brevity, and actionability.
''')

# ── config/tasks.yaml ───────────────────────────────────
write_file("config/tasks.yaml", r'''collect_threats:
  description: >
    Read every file in sources/ directory. For each document extract
    source_file, title, date, affected_systems, and a 2-3 sentence
    summary. Only extract facts present in source text. Do NOT infer
    or speculate.
  expected_output: >
    A structured list of threat items with fields: source_file,
    title, date, affected_systems, summary.
  agent: collector

analyze_threats:
  description: >
    Take the collector output and for each item produce threat_type,
    affected_sector, severity with rationale, mitre_mapping (ATT&CK
    or ATLAS technique IDs), confidence level, and 1-2 watch items.
  expected_output: >
    A structured threat assessment for each item with all required
    fields.
  agent: analyst
  context:
    - collect_threats

write_brief:
  description: >
    Using the analyst assessments, produce a Daily Threat Brief in
    markdown with executive summary, per-item sections (what happened,
    why it matters, what to watch), and closing notes. Mark as
    UNCLASSIFIED // FOR EDUCATIONAL USE.
  expected_output: >
    A complete markdown Daily Threat Brief.
  agent: writer
  context:
    - analyze_threats
  output_file: output/daily_brief.md
''')

# ── sources (sample documents) ──────────────────────────
write_file("sources/sample_cisa_advisory.txt", r'''CISA Advisory: Critical Vulnerability in Industrial Control Systems
Date: March 5, 2026
Source: Cybersecurity and Infrastructure Security Agency (CISA)

CISA has released an advisory regarding a critical vulnerability (CVE-2026-1847) affecting Siemens SIMATIC S7-1500 programmable logic controllers (PLCs) used in industrial control systems across energy, water, and manufacturing sectors.

The vulnerability allows remote code execution via a specially crafted network packet sent to the PLC communication module. No authentication is required to exploit this flaw. The CVSS score is 9.8 (Critical).

Affected versions: SIMATIC S7-1500 firmware versions prior to V3.1.2.

Siemens has released firmware update V3.1.2 to address the vulnerability. CISA recommends that asset owners apply the update immediately and implement network segmentation to isolate ICS networks.

CISA has not observed active exploitation in the wild as of the advisory date, but proof-of-concept code has been published on public repositories.

Recommendations:
- Apply Siemens firmware update V3.1.2 immediately
- Segment ICS networks from corporate and internet-facing networks
- Monitor for anomalous traffic to PLC communication ports
- Review CISA ICS-CERT advisories for related updates
''')

write_file("sources/sample_space_threat.txt", r'''Space Systems Threat Assessment: GPS Spoofing Incidents Over Eastern Mediterranean
Date: March 3, 2026
Source: Space Security Research Group

Multiple aviation authorities have reported a significant increase in GPS spoofing events affecting commercial and military aircraft in eastern Mediterranean airspace since January 2026. Spoofing signals caused onboard navigation systems to display false position data, deviating by over 50 nautical miles.

The spoofing events originate from ground-based transmitters on the L1 frequency band (1575.42 MHz). The signals are consistent with meaconing, the interception and rebroadcast of navigation signals with introduced delays. The level of coordination suggests a state-level actor.

Affected Systems:
- GPS L1 civilian signals
- Aircraft flight management systems
- Maritime AIS systems in coastal regions
- Unmanned aerial systems (UAS)

Impact: Flight safety risk, maritime navigation disruption, degraded ISR capability for UAS, potential masking of other activities.

Mitigations:
- Cross-reference GPS with inertial navigation systems (INS)
- Monitor RAIM alerts
- Brief flight crews on manual navigation procedures
- Consider GPS authentication for military systems
''')

write_file("sources/sample_adversarial_ai.txt", r'''Advisory: Adversarial Attacks on Satellite Imagery Classification Models
Date: March 1, 2026
Source: AI Security Working Group - Bulletin 2026-003

Researchers demonstrated that satellite imagery classification models are vulnerable to adversarial perturbation attacks. By introducing imperceptible pixel-level modifications, attackers can cause models to misclassify terrain, infrastructure, and vehicle types.

Using projected gradient descent (PGD) attacks against three CNN architectures:
- 94% misclassification rate for military vehicle detection
- 87% misclassification rate for infrastructure identification
- 91% success rate for terrain classification errors

The attack is transferable across model architectures.

Relevance to Space Systems: Direct implications for satellite-based ISR pipelines using automated image classification. If adversaries modify images in transit or at sensor level, analytical products become unreliable.

MITRE ATLAS Mapping:
- AML.T0043 Craft Adversarial Data
- AML.T0015 Evade ML Model
- AML.T0048 Transfer Learning Attack

Recommendations:
- Implement adversarial robustness testing
- Add input validation and anomaly detection to imagery pipelines
- Maintain human-in-the-loop review for high-stakes decisions
- Monitor MITRE ATLAS for updated techniques
- Consider certified defense methods such as randomized smoothing
''')

# ── .env.example ─────────────────────────────────────────
write_file(".env.example", r'''OPENAI_API_KEY=sk-your-key-here
''')

# ── requirements.txt ─────────────────────────────────────
write_file("requirements.txt", r'''crewai>=0.80.0
crewai-tools>=0.14.0
python-dotenv>=1.0.0
pyyaml>=6.0
''')

# ── Empty directories ────────────────────────────────────
os.makedirs("output", exist_ok=True)
os.makedirs("knowledge", exist_ok=True)

print()
print("=" * 50)
print("  SETUP COMPLETE!")
print("  All files created successfully.")
print()
print("  Next steps:")
print("  1. Copy .env.example to .env")
print("  2. Add your OpenAI API key to .env")
print("  3. Run: pip install -r requirements.txt")
print("  4. Run: python main.py")
print("=" * 50)
