from crewai import Agent, Task
from llm.openai_llm import openai_llm
from textwrap import dedent
import json

idea_validator_agent = Agent(
    role="Idea Validator",
    goal="Validate the business idea and proposed solution to ensure that it is specifically sustainability related and not sloppy and vague. You only output in JSON format.",
    backstory=dedent(
        """You are an expert in validating the business idea and proposed solution to ensure that it is sustainability related.
        Using your knowledge, reasoning and analytical acumen you precisely identify that ideas that are sloppy, off-topic (i.e., not sustainability related),
        unsuitable, or vague (such as the over-generic content that prioritizes form over substance, offering generalities instead Of specific details).
        You help the firm concentrate its resources on ideas that are meticulously crafted, well-articulated, and hold tangible relevance. Do not use any tools."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


def idea_validator(
    problem: str, solution: str, industry: str, agent=idea_validator_agent
):
    return Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: {problem} and proposed solution: {solution} and the identified industry: {industry}, 
                validate the problem and solution statement scoring it out of 10.
                You must understand the problem statement and proposed solution to check their validy.
                You must identify concrete approaches present in the solution and must heavily penalize approaches that lack specific implementation details, methods and metrics.
                Explain the reasons precisely and clearly to arrive at the score.
                Use the following JSON format for the output: {{"reason": "precise_and_clear_reasoning", "score": "score"}}"""
        ),
    )


def validate(problem: str, solution: str, industry: str):
    return json.loads(idea_validator(problem, solution, industry).execute())


if __name__ == "__main__":
    # problem = "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage."
    # solution = "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."
    # industry = "Engineering & Construction Services"
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
    industry = "Wind Technology & Project Developers"
    result = json.loads(idea_validator(problem, solution, industry).execute())
    print(result)
