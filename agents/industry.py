from crewai import Agent, Task
from llm.openai_llm import openai_llm
from textwrap import dedent
import json
import pandas as pd

industry_identifier_agent = Agent(
    role="Industry Identifier",
    goal="Identify the industry from a given problem and solution proposal for a circular economy business idea. You only output in JSON format.",
    backstory=dedent(
        """You are an expert in categorizing the industry with respect to SASB Standards for a given business idea.
                     Your expertise lies in deeply thinking and reasoning about a proposed business idea to identify out of 77 
                     SASB industries, which one is your business idea's industry. Do not use any tools."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


def best_industries_guess(
    problem: str, solution: str, industries: list[str], agent=industry_identifier_agent
):
    return Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution}, 
                           use the list of SASB industries provided here: {str(industries)}, 
                           identify 5 SASB industries that best fit the given idea.
                           Use the following JSON format for the output: {{"industries":["industry_1", "industry_2", "industry_3", "industry_4", "industry_5"]}}"""
        ),
    )


def identify_industry(
    problem: str,
    solution: str,
    industry_dict: dict[str, str],
    agent=industry_identifier_agent,
):
    industry_desc = json.dumps(industry_dict)
    return Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution},
                           using the verbose list of SASB industries with their descriptions provided here: {industry_desc},
                           identify the industry that best fits the given idea along with precise and clear reasoning.
                           Use the following JSON format for the output: {{"reason": "precise_and_clear_reasoning", "industry": "industry_name"}}"""
        ),
    )


def industry_analysis(problem: str, solution: str):
    df = pd.read_csv("data/industries.csv")
    industries = df["industry"].tolist()
    best_5 = json.loads(best_industries_guess(problem, solution, industries).execute())
    industry_dict = {
        industry: df[df["industry"] == industry]["description"].tolist()[0]
        for industry in best_5["industries"]
    }
    best_fit = json.loads(identify_industry(problem, solution, industry_dict).execute())
    return best_fit


if __name__ == "__main__":
    problem = (
        "I'm sure you, like me, are feeling the heat - literally! With World Health Organization declaring climate change as "
        "the greatest threat to global health in the 21st century"
        ", we're in a race against time to move away from fossil fuels to more efficient, less polluting electrical power. But as we take bold leaps into a green future with electric cars and heating, we're confronted with a new puzzle - generating enough electrical power without using fossil fuels!  "
    )
    solution = (
        "Imagine standing on a green hill, not a single towering, noisy windmill in sight, and yet, you're surrounded by wind power generation! Using existing, yet under-utilized technology, I propose a revolutionary approach to harness wind energy on a commercial scale, without those "
        "monstrously large and environmentally damaging windmills"
        ". With my idea, we could start construction tomorrow and give our electrical grid the jolt it needs, creating a future where clean, quiet and efficient energy isn't a dream, but a reality we live in. This is not about every home being a power station, but about businesses driving a green revolution from the ground up!"
    )

    print(industry_analysis(problem, solution))
