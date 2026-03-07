import os
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
