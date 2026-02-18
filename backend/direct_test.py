from openai import OpenAI

# Paste your full Groq key here manually:
client = OpenAI(
    api_key="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",  # Replace with your actual key
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # smaller model that most accounts have access to
    messages=[{"role": "user", "content": "Hello from test"}]
)

print("Response from Groq:", response.choices[0].message.content)
