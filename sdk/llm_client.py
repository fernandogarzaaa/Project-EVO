import os
from openai import OpenAI

# Initialize client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "sk-placeholder"),
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:7870/v1") 
)

def query_agent(prompt, role="system"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": role, "content": "You are a specialized agent in Project Evo. Respond with precision."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
