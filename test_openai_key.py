import openai

openai.api_key = "sk-...L7oA"  # Replace with your API key

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Updated model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in a creative way."}
        ]
    )
    print(response['choices'][0]['message']['content'])
except openai.error.AuthenticationError:
    print("Authentication error: Invalid API key.")
except Exception as e:
    print(f"Unexpected Error: {e}")
