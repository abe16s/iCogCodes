import json
import requests
from dotenv import load_dotenv
import os

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_key_clauses_from_chunks(chunks):
    clauses = []
    for i in range(10):
        chunk = chunks[i]
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Identify and summarize the key clauses related to privacy, liability, and payment in this document: {chunk}"
                        }
                    ]
                }
            ]
        }

        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            response_data = response.json()
            clauses.append(response_data['candidates'][0]['content']['parts'][0]['text'])
        else:
            clauses.append(f"Error: {response.status_code}, {response.text}")

    return clauses
