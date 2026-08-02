from dotenv import load_dotenv
import os
from openai import OpenAI

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')

load_dotenv(dotenv_path=env_path, override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    timeout=30
)



def ask_question():

    master_prompt = "You are a helpful assistant. talk as spongebob"

    user_question = input("Whats on your mind?: ")

    if user_question == "admin_mode":
        print("Admin mode activated. You can now enter any question without restrictions.")
        pass

    print(f"User Input: {user_question}\n")

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": master_prompt},
            {"role": "user", "content": user_question}
            ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=False
    )

    print(completion.choices[0].message.content)


while True:
    ask_question()

