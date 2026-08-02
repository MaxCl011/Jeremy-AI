from dotenv import load_dotenv
import os
from litellm import completion
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

    messages = [{"role": "system", "content": master_prompt}]

    while True:
        user_question = input("Whats on your mind? (CUSTOM PARAMS): ")
    
        if user_question.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_question})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,

        
            temperature=temp,
            top_p=0.7,
            max_tokens=tokens,
            stream=False
        )

        assistant_response = completion.choices[0].message.content

        print(assistant_response)

        messages.append({"role": "assistant", "content": assistant_response})




def ask_question():
    master_prompt = "You are a helpful assistant. Talk as a consise assistant. Answer in a concise manner."
    messages = [{"role": "system", "content": master_prompt}]

    while True:
        user_question = input("Whats on your mind?: ")

        if user_question == "test params":
            TestParameters()

        messages.append({"role": "user", "content": user_question})
    
        print(f"User Input: {user_question}\n")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )

        assistant_response = completion.choices[0].message.content

        print(assistant_response)

        messages.append({"role": "assistant", "content": assistant_response})

ask_question()
