

from jemma.modelInteraction import modelInteraction


def startCodeSession(firstPrompt : str):
    try:
     with open('.current_chat.txt', "w") as f:
        f.write('USER'+firstPrompt)
        model_Response = modelInteraction(firstPrompt)
        f.write('YOU(MODEL)'+model_Response)
        print(model_Response)
        continueChat()
    except PermissionError:
       print('Could not strat a chat session')


def continueChat():
    newPrompt = input('>')
    try:
     with open('current_chat.txt', 'w') as f:
        chatHistory = f.read('.current_chat.txt')
        model_Response = modelInteraction(chatHistory + "USER : "+newPrompt)
        f.write('USER : '+newPrompt)
        f.write('YOU(MODEL) : '+model_Response)
        print (model_Response)
        continueChat()


  
   
    
    except FileNotFoundError:
        print('err..., something went wrong')
        print('exiting now, please start a new session')
        quit()