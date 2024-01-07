from crewai import Agent, Task
from llm.openai_llm import openai_llm
from textwrap import dedent
from vectorstore.chroma import ChromaDB
import json

sustainability_agent = Agent(
    role="Environmental Sustainability Inspector",
    goal="Assess the business idea and proposed solution to ensure that it is ecological (climate, water, energy, waste) sustainability related. You only output in JSON format.",
    backstory=dedent(
        """You are an experienced Environmental Sustainability Inspector who specialises in analysisng new business ideas and proposed solutions to ensure that they promote ecological (climate, water, energy, waste) sustainability and circular economy.
        The investment firm you are working at wants to invest in ideas that promote circular economy.
        You help the firm identify key metrics that they need to look for to ensure that their ideas are sustainability related and promote a circular economy.
        Do not use any tools."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


def analyse_sasb_metrics(
    problem: str,
    solution: str,
    industry: str,
    sasb_standards: str,
    agent=sustainability_agent,
):
    return Task(
        agent=agent,
        description=dedent(
            f"""You are given the business idea: {problem} and proposed solution: {solution} in the given industry: {industry}.
            Being extremely focused on topics that are related to CLIMATE, WATER, ENERGY, WASTE, RECYCLING, REDUCE and REUSE sustainability,
            you need to identify 3 key SASB Topics from the Table: SUSTAINABILITY DISCLOSURE TOPICS & METRICS: {sasb_standards} which are relate to environmental (climate, water, energy, waste) sustainability and circular economy. Only stick to the topics column. Topics are usually short and general so look for only that.
            Use the following JSON format for the output: {{"topics": ["topoic_1", "topoic_2", "topoic_3"]}} 
            """
        ),
    )


def analyse_sustainability(problem: str, solution: str, industry: str):
    db = ChromaDB()
    sasb_standards = db.query(
        "Table: SUSTAINABILITY DISCLOSURE TOPICS & METRICS", industry
    )

    sasb_metrics = json.loads(
        analyse_sasb_metrics(problem, solution, industry, sasb_standards).execute()
    )

    return Task(
        agent=sustainability_agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution} in the given industry: {industry},
                           You are given a list of 3 key SASB topics: {sasb_metrics} which you need to generate 3 independent assessments with the help of knowledge you already have.
                           Your assessment should be in the following format:
                           ```
                           1. Highlight the solution portion that is most relavant for a given topic.
                           2. List down the topic and associated metrics in detail and how it is calculated.
                           3. A calculated guess for that topic that is related to the solution and relevant in the industry.
                           ```
                           Now combine all the assessments in one assessment for each topic.

                           Use the following JSON format for the output: {{
                            "topic_1_name": ["assessment_point_1", "assessment_point_2", "assessment_point_3"], 
                            "topic_2_name": ["assessment_point_1", "assessment_point_2", "assessment_point_3"],
                            "topic_3_name": ["assessment_point_1", "assessment_point_2", "assessment_point_3"]
                            }}
                           """
        ),
    )


def assess_sustainability(problem: str, solution: str, industry: str):
    return json.loads(analyse_sustainability(problem, solution, industry).execute())


if __name__ == "__main__":
    problem = "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage."
    solution = "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."
    industry = "Engineering & Construction Services"

    print(assess_sustainability(problem, solution, industry))
