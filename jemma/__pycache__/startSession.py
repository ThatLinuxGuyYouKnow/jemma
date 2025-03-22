def startCodeSession(firstPrompt : str):
    try:
     with open('.current_chat.txt', "w") as f:
        f.write(firstPrompt)
    except PermissionError:
       print('Could not strat a chat session')


def continueChat(newPrompt:str, chatHistory):
    try:
     with open('current_chat.txt', 'r') as f:
        f.read