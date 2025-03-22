import json
import requests

from jemma.main import get_api_key
def modelInteraction(prompt: str):
    apikey = get_api_key()
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt
            }
        ]}]
    }
    
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apikey}",
        headers={'Content-Type': "application/json"},
        data=json.dumps(payload)
    )
    return response
    