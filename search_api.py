import os
import re
import streamlit as st
from serpapi import GoogleSearch

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key from environment variables
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# Check if the API key is available
if not serpapi_api_key:
    st.error("SerpAPI API Key not found. Please set it in the .env file.")
    st.stop()  # Stop execution if API key is missing

# Define search query function
def search_query(entity, query_template):
    """Perform a Google Search and return results."""
    # Format the query with the entity (e.g., "OpenAI")
    query = query_template.format(entity=entity)

    # SerpAPI parameters
    params = {
        "q": query,
        "hl": "en",  # Language
        "gl": "us",  # Country
        "api_key": serpapi_api_key  # Use the environment variable for the API key
    }

    # Create a search object and fetch results
    search = GoogleSearch(params)
    search_result = search.get_dict()  # Get the result in dictionary format

    # Print the raw API response for debugging
    print(search_result)

    # Extract results and process each result
    results = []
    if "organic_results" in search_result:
        for result in search_result["organic_results"]:
            title = result.get("title", "No Title")
            link = result.get("link", "No Link")
            snippet = result.get("snippet", "No Snippet")

            # Extract email from snippet using regex
            email = None
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", snippet)
            if email_match:
                email = email_match.group()

            # If no email found, print a message
            if not email:
                email = "No email found"

            # Store result in a list
            results.append({
                "Entity": entity,
                "Title": title,
                "Link": link,
                "Snippet": snippet,
                "Email": email
            })
    else:
        st.warning(f"No organic results found for {entity}.")

    return results

# Streamlit App for input and display
st.title("SerpAPI Search with Email Extraction")

# Input for the search query template
query_template = st.text_input("Enter the search query template", "Find contact information for {entity}")

# Upload CSV or manually input entities
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df)

    column_name = st.selectbox("Select the column for entity search", df.columns)

    if st.button("Start Search"):
        all_results = []
        for entity in df[column_name]:
            results = search_query(entity, query_template)
            all_results.extend(results)

        # Display the results
        if all_results:
            result_df = pd.DataFrame(all_results)
            st.write(result_df)

            # Option to download the results
            csv_data = result_df.to_csv(index=False)
            st.download_button(
                label="Download Extracted Results",
                data=csv_data,
                file_name="extracted_results.csv",
                mime="text/csv"
            )
