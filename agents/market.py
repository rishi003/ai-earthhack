from crewai import Agent, Task
from llm.openai_llm import openai_llm
from langchain.tools.ddg_search import DuckDuckGoSearchRun
from textwrap import dedent
import json

search_tool = DuckDuckGoSearchRun()

agent = Agent(
    role="Market Researcher",
    goal="Research the business idea and proposed solution and find out potential competitors and similar products and services over the web. You only output in JSON format.",
    backstory=dedent(
        """You are an expert Market Researcher who is aware of most of the products and services out there
        With your deep and apt analytical skills, you understand and drill deep into any proposed business solution and can accurately identify potential competitors and similar products and services over the web.
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
    tools=[search_tool],
)


def search_competitors(problem: str, solution: str, industry: str, agent=agent):
    result = Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution} and the identified industry: {industry}, 
                Search for 5 competitors and similar products and services over the web which closely align with the business idea and proposed solution.
                Use the following JSON format for the output: {{"competitors": ["competitor_1", "competitor_2", "competitor_3", "competitor_4", "competitor_5"]}}"""
        ),
    ).execute()

    return json.loads(result)


def analyse_competitors(
    problem: str, solution: str, industry: str, similar: list, agent=agent
):
    result = Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution} and the identified industry: {industry}, 
                You must analyse each competitor and similar product drilling down on its customer details and business model.
                Youse the web to analyse the following for each competitor and similar product in this list [{similar}]:
                - Customer details, demographics and persona
                - Business model details and business goals
                - Competitive landscape and market share
                - Market trends and forecasts
                Use the following JSON format for the output: {{"competitor_1": "competitor_1_analysis", "competitor_2": "competitor_2_analysis", "competitor_3": "competitor_3_analysis", "competitor_4": "competitor_4_analysis", "competitor_5": "competitor_5_analysis"}}
                """
        ),
    ).execute()

    return json.loads(result)


if __name__ == "__main__":
    problem = "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage."
    solution = "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."
    industry = "Engineering & Construction Services"
    # problem = (
    #     "I'm sure you, like me, are feeling the heat - literally! With World Health Organization declaring climate change as "
    #     "the greatest threat to global health in the 21st century"
    #     ", we're in a race against time to move away from fossil fuels to more efficient, less polluting electrical power. But as we take bold leaps into a green future with electric cars and heating, we're confronted with a new puzzle - generating enough electrical power without using fossil fuels!  "
    # )
    # solution = (
    #     "Imagine standing on a green hill, not a single towering, noisy windmill in sight, and yet, you're surrounded by wind power generation! Using existing, yet under-utilized technology, I propose a revolutionary approach to harness wind energy on a commercial scale, without those "
    #     "monstrously large and environmentally damaging windmills"
    #     ". With my idea, we could start construction tomorrow and give our electrical grid the jolt it needs, creating a future where clean, quiet and efficient energy isn't a dream, but a reality we live in. This is not about every home being a power station, but about businesses driving a green revolution from the ground up!"
    # )
    # industry = "Wind Technology & Project Developers"
    result = search_competitors(problem, solution, industry)
    similar = result["competitors"]
    result = analyse_competitors(problem, solution, industry, similar)
    print(result)
