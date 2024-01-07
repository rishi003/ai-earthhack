import os
import streamlit as st
from dotenv import load_dotenv
from actions.start_analysis import start_analysis

load_dotenv()

# Main page configurations
st.set_page_config(layout="wide", page_title="Shark Tank Assistant AI")

# Title
st.title("Shark Tank Assistant AI")

# Sidebar
st.sidebar.header("Settings")

# Main content
st.subheader("Analyze the idea fit for a circular economy")

# Problem Statement
problem = st.text_area("Enter the problem statement: ")

# Proposed Solution
solution = st.text_area("Enter the proposed solution: ")

# Submit button
if st.button("Drill the Idea!"):
    st.markdown(start_analysis(problem, solution))
