def startCodeSession(firstPrompt : str):
    try:
     with open('./current_chat', "w") as f:
        f.write(firstPrompt)
    except PermissionError:
       print('Could not strat a chat session')
    