from crewai import Agent, Task
from llm.openai_llm import openai_llm
from textwrap import dedent
import pandas as pd
import json

financial_expert_agent = Agent(
    role="Financials Expert",
    goal="Identify environmental impact financials for the business idea. You only output in JSON format.",
    backstory=dedent(
        """You are a financial expert in analyzing circular economy businesses ideas and the financial investment required for implementation. You help the firm identify key metrics that they need to look for to ensure that their ideas are financially viable and promote a circular economy. Do not use any tools."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)


def analyse_industry_finances(
    problem: str,
    solution: str,
    industry: str,
    agent=financial_expert_agent,
):
    task = Task(
        agent=agent,
        description=dedent(
            f"""Your task is to figure out estimated Costs and Investment Requirements for the following business idea in industry ```{industry}``` noted in delimeters below:
            ```
            Problem: {problem}
            Solution {solution}
            ```

            Costs include manufacturing, labor, material, and operational expenses. Investments include initial setup costs and capital expenditure needed for infrastructure and technology.

            List the details for each type of cost with an estimated US dollar for each. Enter only numeric values in USD. Include references for these costs at the end.
            Use the following JSON format for the output: {{"Costs": {{"cost_1_name": "cost_1", "cost_2_name": "cost_2", "cost_3_name": "cost_3"}}, "References": ["ref_1", "ref_2", "ref_3"]}} 
            """
        ),
    )

    result = task.execute()
    return json.loads(result)


def analyse_related_companies_finances(
    problem: str, solution: str, industry: str, agent=financial_expert_agent
):
    # read csv file for related companies financials
    df_iwa_financials = pd.read_csv(
        "data\output-IWA-UpdatedIndustry-dataset.csv", encoding="latin"
    )
    df_iwa_financials = pd.DataFrame(df_iwa_financials)

    # filter for industry
    df_related_company_in_industry = df_iwa_financials[
        df_iwa_financials["GICS Sub-Industry"] == industry
    ]

    # get list of related companies
    related_company_list = df_related_company_in_industry["Company Name"].tolist()

    related_companies = Task(
        agent=agent,
        description=dedent(
            f"""For the given business idea: ```{problem}``` and proposed solution: ```{solution}``` in the given industry: ```{industry}```,
            You are given a list of companies in that industry: ```{related_company_list}``` which you need to determine which companies are most related to the business idea and proposed solution.

            Return a list of 3 companies from that list that are most related to the business idea and proposed solution. Use the following JSON format for the output: {{"companies": ["company_1", "company_2", "company_3"]}}
            """
        ),
    )

    # get list from relate_companies task

    related_companies_list = json.loads(related_companies.execute())["companies"]

    # get data for related companies in dataset
    df_related_companies = df_related_company_in_industry[
        df_related_company_in_industry["Company Name"].isin(related_companies_list)
    ]

    return df_related_companies.to_json(orient="records")


# def combine_financial_analysis(problem: str, solution: str, industry: str):
#     # get data for related companies in dataset
#     df_related_companies = pd.DataFrame(
#         json.loads(analyse_related_companies_finances(problem, solution, industry))
#     )

#     # get data for industry finances
#     df_industry_finances = analyse_industry_finances(
#         problem, solution, industry
#     ).execute()

#     print((json.loads(df_industry_finances)))

#     # combine dataframes
#     df_combined_financials = pd.concat(
#         [df_industry_finances, df_related_companies], axis=1
#     )

#     # convert to json
#     json_combined_financials = df_combined_financials.to_json(orient="records")

#     return json_combined_financials


if __name__ == "__main__":
    problem = "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage."
    solution = "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."
    industry = "Engineering & Construction Services"

    print(analyse_related_companies_finances(problem, solution, industry))
    print(analyse_industry_finances(problem, solution, industry))
