import yaml
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
