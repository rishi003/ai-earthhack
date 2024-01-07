from agents import validity, sustainability, industry, report
import json


def start_analysis(problem, solution):
    """
    The start_analysis function takes in the problem statement and proposed solution and starts analysing the idea with different agents.
    """

    # Industry Analysis
    industry_analysis = industry.industry_analysis(problem, solution)
    industry_name = industry_analysis["industry"]

    # Validity Analysis
    validity_analysis = validity.validate(problem, solution, industry=industry_name)

    # Sustainability Analysis
    sustainability_analysis = sustainability.assess_sustainability(
        problem, solution, industry_name
    )

    # Combined Analysis
    combined_analysis = {
        "industry": industry_analysis,
        "validity": validity_analysis,
        "sustainability": sustainability_analysis,
    }

    # You can directly use the combined_analysis object in streamlit or generate a markdown report using the agent below

    # Report
    generated_report = report.generate(str(combined_analysis))

    return generated_report
