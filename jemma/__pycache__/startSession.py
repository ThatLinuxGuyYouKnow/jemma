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
    except FileNotFoundError:
        print('err..., something went wrong')
        print('exiting now, please start a new session')
        quit()