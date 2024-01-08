import os
import streamlit as st
import json
from dotenv import load_dotenv
from actions.start_analysis import start_analysis
from agents import validity, sustainability, industry, report, financial, market


load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="EcoShark Investor AI Tool", 
    page_icon="🦈", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


#Custom CSS to inject into Streamlit
def add_custom_css():
    st.markdown("""
        <style>
            /* Main content area */
            .main .block-container {
                padding-top: 2rem;
            }
            
            /* Tabs */
            .stTabs > div {
                background-color: white; /* Adjust the tab background color */
            }
            
            /* Buttons */
            .stButton > button {
                border-radius: 20px; /* Rounded corners like in the prototype */
                border: none;
                color: white;
                background-color: #4F8A8B; /* Adjust the button color */
            }
            
            /* Sidebar button */
            .css-18e3th9 {
                display: flex;
                justify-content: center; /* Center button in the sidebar */
                padding: 5px 10px;
                margin: 10px 0;
            }
            
            /* Sidebar itself */
            .css-1d391kg {
                background-color: #04506B; /* Adjust the sidebar color */
                padding: 25px;
            }
            
            /* Download button */
            .download-button {
                background-color: #04506B; /* Adjust the button color */
                color: white;
                border-radius: 20px; /* Rounded corners */
                padding: 10px 24px;
                border: none;
                margin-left: auto;
            }
        </style>
        """, unsafe_allow_html=True)

# Adding the custom CSS to the app
add_custom_css()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the custom CSS
# local_css("check.css")  # You need to create a CSS file with your styles

# Title and logo at the top of the page
col1, col2 = st.columns([1, 10])
with col1:
    st.image("icon.png")  # Replace with the path to your logo image
with col2:
    st.title("EcoShark")

def main_page():
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Sustainability", "Finaces", "Competiton"])
    
    with tab1:
        st.header("Overview")
        
        # The form for inputting the business problem and solution
        with st.form(key='overview_form'):
            investment_problem = st.text_area("Describe the business problem:")
            proposed_solution = st.text_area("Describe the proposed solution:")
            submit_button = st.form_submit_button(label='Get Analysis')

        # When the user submits the form
        if submit_button:
            if investment_problem and proposed_solution:
                # Perform the combined analysis
                generated_report = start_analysis(investment_problem, proposed_solution)
                
                # Assuming the report is a dictionary with keys for each analysis section
                if generated_report:
                    st.success("Combined Analysis Report:")

                    # Display each section of the report
                    if 'industry' in generated_report:
                        st.subheader("Industry Analysis")
                        st.json(generated_report['industry'])

                    if 'validity' in generated_report:
                        st.subheader("Validity Analysis")
                        st.json(generated_report['validity'])

                    if 'sustainability' in generated_report:
                        st.subheader("Sustainability Analysis")
                        st.json(generated_report['sustainability'])

                    if 'competition' in generated_report:
                        st.subheader("Competition Analysis")
                        st.json(generated_report['competition'])
                else:
                    st.error("No data returned from the analysis.")
            else:
                st.warning("Please enter both the business problem and the proposed solution.")

    with tab2:
        st.header("Sustainability")
        
        # The form for inputting the business sustainability problem
        with st.form(key='sustainability_form'):
            investment_problem = st.text_area("Describe the business sustainability problem:")
            proposed_solution = st.text_area("Describe the proposed solution:")
            submit_button = st.form_submit_button(label='Get Sustainability Analysis')

        # When the user submits the form
        if submit_button and investment_problem and proposed_solution:
            # Generate sustainability analysis
            industry_analysis = industry.industry_analysis(investment_problem, proposed_solution)
            industry_name = industry_analysis["industry"]
            
            # Perform the sustainability assessment
            result = sustainability.assess_sustainability(investment_problem, proposed_solution, industry_name)
            
            # Display the result
            st.success("Sustainability Analysis:")
            st.json(result)  # Display the JSON result directly
        elif submit_button:
            st.warning("Please enter a description of the business sustainability problem and the proposed solution.")


# Define tab3 for financial analysis in Streamlit
    with tab3:
        st.header("Financial Analysis")
        
        # Form for financial analysis input
        with st.form(key='financial_analysis_form'):
            problem = st.text_area("Describe the business problem for financial analysis:")
            solution = st.text_area("Describe the proposed solution for financial analysis:")
            submit_button = st.form_submit_button(label='Get Financial Analysis')

        # When the user submits the form
        if submit_button and problem and solution:
            # Perform industry analysis to get the industry name
            industry_analysis = industry.industry_analysis(problem, solution)
            industry_name = industry_analysis["industry"]
            
            # Check if industry name is retrieved successfully
            if industry_name:
                # Perform the financial analysis
                related_companies_finances = financial.analyse_related_companies_finances(problem, solution, industry_name)
                industry_finances = financial.analyse_industry_finances(problem, solution, industry_name)
                
                # Display the financial analysis in the Streamlit app
                st.subheader("Financial Analysis for Related Companies:")
                st.json(related_companies_finances)  # If it's already a dict, no need for json.loads()

                st.subheader("Industry Financial Analysis:")
                st.json(industry_finances)  # If it's already a dict, no need for json.loads()
            else:
                st.error("Unable to determine the industry from the provided problem and solution.")
        elif submit_button:
            st.warning("Please enter the business problem and proposed solution for the financial analysis.")
            

    with tab4:
        st.header("Competition")

        # The form for inputting the business competition problem
        with st.form(key='competition_form'):
            investment_problem = st.text_area("Describe the business sustainability problem:")
            proposed_solution = st.text_area("Describe the proposed solution:")
            submit_button = st.form_submit_button(label='Get Competition Analysis')

        # When the user submits the form
        if submit_button and investment_problem and proposed_solution:
            # Generate competition analysis
            industry_analysis = industry.industry_analysis(investment_problem, proposed_solution)
            industry_name = industry_analysis["industry"]
            
            # Perform the sustainability assessment
            result = market.search_competitors(investment_problem, proposed_solution, industry_name)
            similar = result["competitors"]
            result = market.analyse_competitors(investment_problem, proposed_solution, industry_name, similar)
            
            # Display the result
            st.success("Competition Analysis:")
            st.json(result)  # Display the JSON result directly
        elif submit_button:
            st.warning("Please enter a description of the business competition problem and the proposed solution.")

    # Main content area - could be filled with relevant widgets and content
    st.write("Main content area")

    # Download Report Button
    if st.button('Download Report'):
        st.write("Report downloading...")  # Placeholder for download functionality

# Footer
st.sidebar.text("© 2024 EcoShark Investor AI Tool")

# Run the app
if __name__ == "__main__":
    main_page()
    st.sidebar.text("Welcome to the EcoShark Investor AI Tool!")
    st.sidebar.text("Assisting you in making informed investment decisions.")
    st.sidebar.text("Enter a description of your investment problem and click")
    st.sidebar.text("'Get Analysis'.")
    st.sidebar.text("Disclaimer: This tool provides suggestions and ")
    st.sidebar.text("should not replace professional financial advice.")
    st.sidebar.text("For educational purposes only.")
