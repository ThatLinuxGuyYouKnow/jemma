from jemma.inference import get_model_response
from jemma.agentic_response import AgentResponse
from jemma.response_enums import ResponseType


class AgentLoop():

    def __init__(self):
        self.messages = []    

 
    def start_loop(self, new_message: str, model_id : str):

        ## add the newest message from the user to the message stack

        self.messages.append({'role':'user', 'content': new_message})

        accumulated_tool_calls = {}

        response = get_model_response(messages= self.messages, model_id=model_id)

        while True:

            for delta in response:

                if delta.content:

                    yield AgentResponse(
                        type=ResponseType.TEXT,
                        content=delta.content
                    )

                if delta.tool_calls:

                     for tool_call in delta.tool_calls:

                        idx = tool_call.index

                        if idx in accumulated_tool_calls:

                            ## in this case, we've already seen some of this tool call in a previous chunk, we just want to update the funcs args

                            accumulated_tool_calls[idx]["arguments"] += tool_call.function.arguments

                        else:

                            ## we havent seen this function before, we need to start to accumulate it

                            accumulated_tool_calls[idx] = {

                        "id":tool_call.id,
                        "name":tool_call.function.name or '',
                        "arguments": tool_call.function.arguments
                    }
                            
                if accumulated_tool_calls:

                    for tool_call in accumulated_tool_calls:


                        yield AgentResponse(
                            type= ResponseType.TOOL_CALL,
                            content= tool_call['name'] 
                    )
                        
                    try ToolOrchestrator.execute():
                        ## do some stuff if successful, like yield the result of the tc

                    catch 




           




