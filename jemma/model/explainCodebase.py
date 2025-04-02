from configparser import Error
import requests
import json
from requests.exceptions import RequestException
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import errorText, responseFormatter, warningText

def explainCode(directoryStructure: str, apikey: str, files: str):
 try :
    if not apikey or not directoryStructure or not files:
        print(errorText('somethings wrong here'))
        quit()
    model_prompt = """"""
 
    response= modelInteraction()
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apikey}",
        headers={'Content-Type': "application/json"},
        data=json.dumps(payload)
    )
    
    response_data = response.json()
 
    if response.status_code == 400:
        print(errorText("Your api key likely isn't valid, run " +warningText("gemma-configure ")+ errorText("to enter a new one")))
        return None
    if response.status_code != 200:
        print(errorText("Something went wrong with your request, try again"))
        return None
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        response=  response_data['candidates'][0]['content']['parts'][0]['text']
        print(responseFormatter(response))
    else:
       print(errorText("An error occured and the model did not return a response"))
 except RequestException:
    print(errorText('You need a working Internet connection to use jemma'))
 except Exception as e:
    print(errorText('an error occured, please try again'))
 
