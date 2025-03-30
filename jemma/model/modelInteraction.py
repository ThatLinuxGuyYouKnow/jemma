import json
import requests

from jemma.utils.getApiKey import get_api_key
from jemma.utils.terminalPrettifier import errorText, warningText
from requests.exceptions import RequestException 
def modelInteraction(prompt: str):
 try:
    apikey = get_api_key()
    payload = {
         "system_instruction": {
      "parts": [
        {
          "text": "You are Jemma, a command line coding assistant. Make sure your responses are always helful, firendly, and concise"
        }
      ]
    },
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
 
    if response.status_code == 400:
       print(errorText("Error occured, Your api key likely isn't valid, run")+warningText(' jemma-configure ')+ errorText('to re-enter your key'))
       return None
    if response.status_code != 200:
        print(errorText('An error occured, please try again in a bit'))
        print (str(response.status_code))
        return None
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        response=  response_data['candidates'][0]['content']['parts'][0]['text']
        return response
    else:
        print(errorText('something went wrong and the model did not return a response'))    
        return None  
 except RequestException:
    print(errorText("You need a working Internet Connection to use jemma"))
    return None
 except Exception as e:
    print(errorText('An unexpected error occured, please try again' + str(e)))
    return None