import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.choices[0].message.content)
