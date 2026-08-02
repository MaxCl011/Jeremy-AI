from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("NIM_api_key")

if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

completion = client.chat.completions.create(
    model="meta/llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False
)

print(completion.choices[0].message.content)