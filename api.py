from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import feedparser
import re

app = FastAPI(title="Space Cyber Crew API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RSS_FEEDS = [
    ("CISA Advisories", "https://www.cisa.gov/news-events/cybersecurity-advisories/all.xml"),
    ("CISA Alerts", "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
]

KEYWORDS = [
    "satellite",
    "space",
    "ground station",
    "communications",
    "network",
    "infrastructure",
    "critical infrastructure",
    "cyber",
    "vulnerability",
    "scanning",
    "vendor",
    "supply chain",
    "authentication",
]

class SignalInput(BaseModel):
    source: str
    title: str
    summary: str
    link: str | None = ""

def clean_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split())

def score_signal(title: str, summary: str) -> int:
    text = f"{title} {summary}".lower()
    score = 0
    for keyword in KEYWORDS:
        if keyword in text:
            score += 1
    return score

@app.get("/")
def root():
    return {"status": "ok", "message": "Space Cyber Crew API is running"}

@app.get("/api/signals")
def get_signals():
    results = []

    for source_name, url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:15]:
            title = clean_html(entry.get("title", ""))
            summary = clean_html(entry.get("summary", "") or entry.get("description", ""))
            link = entry.get("link", "")

            score = score_signal(title, summary)

            results.append({
                "source": source_name,
                "title": title,
                "summary": summary[:300] + ("..." if len(summary) > 300 else ""),
                "link": link,
                "score": score
            })

    # Sort by relevance score, then keep top results
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Remove very weak items if possible
    filtered = [item for item in results if item["score"] > 0]

    return filtered[:8] if filtered else results[:8]

@app.post("/api/generate-brief")
def generate_brief(signal: SignalInput):
    text = f"{signal.title} {signal.summary}".lower()

    if "vendor" in text or "supply chain" in text:
        domain = "Supply Chain / Third-Party Risk"
        priority = "Medium-High"
        action = "Review vendor dependencies, check connected services, and monitor for follow-on indicators."
    elif "authentication" in text or "login" in text or "credential" in text:
        domain = "Mission Support Systems"
        priority = "Medium"
        action = "Audit authentication logs, review failed access patterns, and verify privileged account controls."
    elif "scanning" in text or "exposed" in text or "network" in text:
        domain = "Ground Station / Communications Layer"
        priority = "Medium-High"
        action = "Review exposed services, validate access controls, and monitor for reconnaissance or enumeration activity."
    elif "vulnerability" in text or "advisory" in text:
        domain = "Space-Adjacent Infrastructure"
        priority = "Medium"
        action = "Assess exposure, map affected systems, and prioritize remediation based on operational relevance."
    else:
        domain = "Space Communications / Supporting Infrastructure"
        priority = "Medium"
        action = "Validate the signal, correlate with related reporting, and assess whether continued monitoring is warranted."

    brief_title = f"Analyst Review: {signal.title}"

    brief_summary = (
        f"This signal may indicate emerging cyber risk relevant to space-supporting infrastructure, "
        f"communications systems, or operational dependencies. Additional validation and correlation "
        f"would be required to determine operational significance."
    )

    return {
        "title": brief_title,
        "summary": brief_summary,
        "priority": priority,
        "domain": domain,
        "action": action,
        "source": signal.source,
        "link": signal.link
    }
