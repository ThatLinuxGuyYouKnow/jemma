from jemma.main.inference.main import get_model_response 


class AgentLoop():

    def __init__(self):
        self.messages = []    

 
    def start_loop(self, new_message: str):

        self.messages.append(new_message)

        response = get_model_response(messages= self.messages)

        if response.tool_calls:



