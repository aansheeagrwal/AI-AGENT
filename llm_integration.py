from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Fetch OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key


def process_with_llm(snippet, query_template):
    """
    Process a snippet using OpenAI's GPT API to extract specific information.
    Args:
        snippet (str): The snippet or content to process.
        query_template (str): A template describing what information to extract.
    Returns:
        str: Extracted or processed information from LLM.
    """
    try:
        # Construct the prompt
        prompt = f"Use the following template to process the text:\n\n{query_template}\n\nText:\n{snippet}\n\nExtracted Information:"

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a newer model
            messages=[
                {"role": "system", "content": "You are an intelligent assistant for parsing information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Adjust based on the expected length of the response
        )

        # Extract the output text
        result = response["choices"][0]["message"]["content"].strip()
        return result

    except openai.error.AuthenticationError:
        return "Error: Authentication failed. Please check your API key."
    except openai.error.OpenAIError as e:
        return f"Error: Something went wrong with the OpenAI API. Details: {str(e)}"

