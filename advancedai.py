from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import re
from datetime import datetime

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

MEMORY_FILE = os.path.join(script_dir, 'memory.json')

#Memort database functions

def load_memorys():
    """Load memorys from json file"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error reading memory file.")
                return []
    return [] 

def save_memorys(fact, event_time=""):
    """Saves a memory as a json file"""
    memorys = load_memorys()
    logged_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = {
        "id": len(memorys) + 1,
        "logged_at": logged_timestamp,
        "fact": fact,
        "event_time": event_time if event_time else "Not Specified"
     }

     memories.append(New_entry)
     with open(MEMORY_FILE, 'W', encodings='utf-8') as f:
        json.dump(memories, f, indent=4)

    print(f"[JSON Memory Created]: Saved '{fact}' (For: {new_entry['event_time']})")

def decide_intent(user_input):
    """Asks a fast AI call to classify whether we need to SAVE, SEARCH, or just CHAT."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    router_prompt = (
        f"Current Time: {current_time}\n"
        "Analyze the user's message and categorize it into ONE of these three actions:\n"
        "1. SAVE - If the user is sharing an appointment, event, fact, or detail they want remembered for the future.\n"
        "2. SEARCH - If the user is asking a question about when, where, or what an event/appointment is, requiring a memory lookup.\n"
        "3. CHAT - If it's a general question, greeting, or conversation that doesn't involve storing or looking up personal memories.\n\n"
        "Respond with ONLY a JSON object in this exact format, with no extra text:\n"
        '{"action": "SAVE" or "SEARCH" or "CHAT", "extracted_fact": "Summary of fact to save (or empty string)", "event_time": "YYYY-MM-DD HH:MM or description (or empty string)"}'
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": router_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"action": "CHAT", "extracted_fact": "", "event_time": ""}



def TestParameters():
    temp = float(input("Enter temperature: "))
    tokens = int(input("Enter max tokens: "))

    master_prompt = "You are a helpful assistant. Talk as a consise assistant. Answer in a concise manner."

    user_question = input("Whats on your mind? (CUSTON PARAMS): ")

    

    

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
