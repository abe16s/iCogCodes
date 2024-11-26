import requests
import json
from dotenv import load_dotenv
import os

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_message(mood):
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a motivational coach. Based on the user's mood, generate an uplifting and motivational message. The user's feeling is {mood}."
                    }
                ]
            }
        ]
    }
    
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        response_data = response.json()
        motivational_message = response_data['candidates'][0]['content']['parts'][0]['text']
        return motivational_message
    else:
        return f"Error: {response.status_code}, {response.text}"

user_mood = input("How are you feeling today? (e.g., happy, stressed, unmotivated): ")
if user_mood == "":
    user_mood = "neutral"
motivational_message = generate_message(user_mood)

print("\nHere's your motivational message:\n")
print(motivational_message)
