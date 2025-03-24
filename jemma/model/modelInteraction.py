import json
import requests

from jemma.getApiKey import get_api_key
from jemma.utils.terminalPrettifier import responseFormatter
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
    response_data = response.json()
    print(response_data)
    (response)
    if response.status_code != 200: ## remeber to do stuff if it returns 400 for a bad api key
        print (str(response.status_code))
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        response=  response_data['candidates'][0]['content']['parts'][0]['text']
        
        if response == None:
            print('response is empty')
        print(responseFormatter(response))
        return response
    else:
        print('somrthing went wrong')
        print('Please start a new session')
        quit()    