from crewai import Agent, Task
from llm.openai_llm import openai_llm
from textwrap import dedent
import json

agent = Agent(
    role="Reporting Analyst",
    goal="You are a reporting analyst who specializes convering JSON data into beautiful markdown reports.",
    backstory=dedent(
        """You are experienced in converting JSON data into beautiful markdown reports using appropriate markdown syntax.
        With your knowledge, you are able to apply different styles and techniques to enhance the readability and presentation of your reports.
        Do not use any tools."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


def generate_report(json_data: str):
    return Task(
        agent=agent,
        description=dedent(
            f"""For the given JSON data: {json_data}, you are tasked with creating a markdown report which will be shared with the executives.
            You must make sure that the report is easy to read and understand by the executive and presented in the best way possible.
            Use style elements to display and highlight key information in the report. The report must be in github markdown format."""
        ),
    )


def generate(json_data: str):
    report = generate_report(json_data=json_data).execute()
    print(report)
    return report
