import requests


def startCodeSession(firstPrompt : str):
    try:
     with open('.current_chat.txt', "w") as f:
        f.write(firstPrompt)
    except PermissionError:
       print('Could not strat a chat session')


def continueChat(newPrompt:str):
    try:
     with open('current_chat.txt', 'r') as f:
        chatHistory = f.read('.current_chat.txt')
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
    
    except FileNotFoundError:
        print('err..., something went wrong')
        print('exiting now, please start a new session')
        quit()