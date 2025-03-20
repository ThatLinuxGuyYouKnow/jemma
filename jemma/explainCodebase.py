import requests
import json

def explainCode(prompt: str, apikey: str, files: str):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt + files}
                ]
            }
        ]
    }
    
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apikey}",
        headers={'Content-Type': "application/json"},
        data=json.dumps(payload)
    )
    
    response_data = response.json()
    
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error generating documentation: {response_data.get('error', 'Unknown error')}"