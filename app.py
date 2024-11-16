# Import necessary libraries
import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import serpapi
from serpapi.google_search import GoogleSearch

from dotenv import load_dotenv
import os
import re
from llm_integration import process_with_llm  # LLM processing (e.g., OpenAI API)

# Load environment variables from .env file
load_dotenv()

# Fetch the SerpAPI key from the environment
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# Streamlit app title
st.title("AI Agent: Search and LLM Integration")

# Option to upload CSV or connect to Google Sheets
option = st.radio("Choose Data Source", ("Upload CSV File", "Connect to Google Sheets"))

# Initialize the DataFrame
df = None

### **Step 1: Handle Data Input (CSV or Google Sheets)**
# If user selects "Upload CSV File"
if option == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)

        # Display data preview
        st.write("Data Preview:")
        st.dataframe(df)

        # Column selection for entity search
        column_name = st.selectbox("Select the column for search (e.g., Company Names)", df.columns)
        st.write(f"Selected Column: {column_name}")

# If user selects "Connect to Google Sheets"
elif option == "Connect to Google Sheets":
    try:
        # Load credentials from JSON file
        credentials = service_account.Credentials.from_service_account_file(
            "credentials.json",  # Path to your credentials.json file
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        # Authorize and connect to Google Sheets
        client = gspread.authorize(credentials)

        # Ask user for the Google Sheet URL
        sheet_url = st.text_input("Enter the Google Sheet URL")

        if sheet_url:
            # Open the Google Sheet by URL
            sheet = client.open_by_url(sheet_url)
            worksheet = sheet.get_worksheet(0)  # Default is first sheet

            # Get all records and convert to DataFrame
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)

            # Display data preview
            st.write("Data Preview from Google Sheets:")
            st.dataframe(df)

            # Column selection for entity search
            column_name = st.selectbox("Select the column for search (e.g., Company Names)", df.columns)
            st.write(f"Selected Column: {column_name}")

    except Exception as e:
        st.error("Error connecting to Google Sheets. Please check your credentials or sheet URL.")
        st.error(str(e))

### **Step 2: Input Query Template**
query_template = st.text_input("Enter the search query template", "Find the email address of {entity}")

### **Step 3: Perform Search and LLM Processing**
if df is not None:
    if st.button("Start Search"):
        results = []  # To store search results
        llm_results = []  # To store LLM processed outputs

        # Loop through each entity in the selected column
        for entity in df[column_name]:
            # Call the SerpAPI for each entity using the search query template
            search = GoogleSearch({
                "q": query_template.format(entity=entity),
                "location": "Austin, Texas",  # Example location, adjust as needed
                "api_key": serpapi_api_key
            })

            # Get results from the search API
            search_result = search.get_dict()
            if search_result:
                snippets = search_result.get("organic_results", [])  # Adjust based on API response format
                for snippet in snippets:
                    results.append({
                        "Entity": entity,
                        "Title": snippet.get("title", "No Title"),
                        "Snippet": snippet.get("snippet", "No Snippet"),
                        "Link": snippet.get("link", "No Link")
                    })

        # Display search results
        if results:
            st.write("Search Results:")
            results_df = pd.DataFrame(results)
            st.dataframe(results_df)

            # Pass snippets to LLM for processing
            st.write("Processing search results with LLM...")
            for result in results:
                snippet = result["Snippet"]
                extracted_info = process_with_llm(snippet, query_template)

                # Add LLM-processed result to list
                llm_results.append({
                    "Entity": result["Entity"],
                    "Snippet": snippet,
                    "Extracted Info": extracted_info
                })

            # Display processed results
            if llm_results:
                llm_results_df = pd.DataFrame(llm_results)
                st.write("Extracted Information from LLM:")
                st.dataframe(llm_results_df)

                # Option to download the results
                csv_data = llm_results_df.to_csv(index=False)
                st.download_button(
                    label="Download Extracted Results as CSV",
                    data=csv_data,
                    file_name="extracted_results.csv",
                    mime="text/csv",
                )
        else:
            st.warning("No search results found.")





