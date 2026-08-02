from dotenv import load_dotenv
import os
from openai import OpenAI
from pymsgbox import prompt

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

def TestParameters():
    temp = float(input("Enter temperature: "))
    tokens = int(input("Enter max tokens: "))
    

    master_prompt = input("Enter master prompt: ")
    user_question = input("Whats on your mind? (CUSTON PARAMS): ")

    while True:
        user_question = input("Whats on your mind? (CUSTOM PARAMS): ")

    

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": master_prompt},
            {"role": "user", "content": user_question}
            ],


        
        temperature=temp,
        top_p=0.7,
        max_tokens=tokens,
        stream=False
    )

    print(completion.choices[0].message.content)




def ask_question():

    master_prompt = "You are a helpful assistant. Talk as a consise assistant. Answer in a concise manner."

    user_question = input("Whats on your mind?: ")

    if user_question == "test params":
        TestParameters()
    
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