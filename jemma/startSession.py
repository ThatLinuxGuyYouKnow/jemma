from jemma.modelInteraction import modelInteraction


def startCodeSession(firstPrompt: str):
    try:
        # Write initial user prompt to the chat history file
        with open('.current_chat.txt', "w") as f:
            f.write('USER: ' + firstPrompt + '\n')
        
        # Get model response
        model_response = modelInteraction(firstPrompt)
        
        # Append model response to chat history
        if model_response:
            with open('.current_chat.txt', "a") as f:
                f.write('YOU(MODEL): ' + model_response + '\n')
            
            print(model_response)
            continueChat()
        
    except PermissionError:
        print('Could not start a chat session - permission error')
    except Exception as e:
        print(f'Error starting chat session: {str(e)}')

def continueChat():
    newPrompt = input('> ')
    
    try:
        # Read existing chat history
        with open('.current_chat.txt', 'r') as f:
            chatHistory = f.read()
        
        # Get model response based on history and new prompt
        model_response = modelInteraction(chatHistory + "USER: " + newPrompt)
        
        # Append new user prompt and model response to chat history
        if model_response:
            with open('.current_chat.txt', 'a') as f:
                f.write('USER: ' + newPrompt + '\n')
                f.write('YOU(MODEL): ' + model_response + '\n')
            
            print(model_response)
            continueChat()
        
    except FileNotFoundError:
        print('Error: Chat history file not found')
        print('Exiting now, please start a new session')
        quit()
    except Exception as e:
        print(f'Error continuing chat: {str(e)}')
        print('Exiting now, please start a new session')
        quit()