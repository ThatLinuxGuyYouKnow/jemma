import requests
import json

from jemma.utils.terminalPrettifier import responseFormatter

def explainCode(directoryStructure: str, apikey: str, files: str):
    if not apikey or not directoryStructure or not files:
        print('somethings wrong here')
        quit()
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": 'Explain the following codebase, mentioning frameworks, languages, critical operating logic, and  only if you find any, critical bugs' + 'Directory Structure'+directoryStructure+'Content: '+ files}
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
 
    if response.status_code != 200:
        print (str(response.status_code))
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        response=  response_data['candidates'][0]['content']['parts'][0]['text']
        if response == None:
            print('response is empty')
        print(responseFormatter(response))
    else:
        return f"Error generating documentation: {response_data.get('error', 'Unknown error')}"