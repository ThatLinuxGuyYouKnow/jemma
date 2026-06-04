import logging
from jemma.inference import get_model_response
from jemma.agentic_response import AgentResponse
from jemma.response_enums import ResponseType
from jemma.services.tool_service import ToolOrchestrator
from jemma.message_enum import MessageType

logger = logging.getLogger("jemma.agent.loop")
logger.setLevel(logging.DEBUG)

class AgentLoop():

    _loop_count = 0

    def __init__(self):
        self.messages = []    

 
    def start_loop(self, new_message: str | None, conversation_history: list | None, model_id : str, message_type: MessageType ):

        AgentLoop._loop_count += 1
        loop_num = AgentLoop._loop_count
        logger.info(f"{'='*40} LOOP {loop_num} {'='*40}")
        logger.info(f"  message_type : {message_type.value}")
        logger.info(f"  model_id     : {model_id}")
        logger.info(f"  new_message  : {new_message}")

        self.messages = conversation_history if conversation_history else []

        ## add the newest message from the user/ tool call result to the message stack

        self.messages.append({'role':message_type.value, 'content': new_message})
        logger.info(f"  message_stack_size: {len(self.messages)}")

        accumulated_tool_calls = {}

        response = get_model_response(messages= self.messages, model_id=model_id)

        full_assistant_text : str = ''

        for delta in response:

                if delta.content:

                    full_assistant_text += delta.content

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

            logger.info(f"  tool_calls_found: {list(tc['name'] for tc in accumulated_tool_calls.values())}")

            self.messages.append({'role':'assistant',
                                       'content':full_assistant_text,
                                       'tool_call': accumulated_tool_calls})

            for tool_call in accumulated_tool_calls.values():


                yield AgentResponse(
                            type= ResponseType.TOOL_CALL,
                            content= tool_call['name'] 
                    )
                        
                   

            tool_results: list = ToolOrchestrator().execute_tool_calls(accumulated_tool_calls= accumulated_tool_calls)
            logger.info(f"  tool_results: {tool_results}")

             ## start a recursive loop IF we have tool call results (or errors)

            logger.info(f"  recursing into loop (next call will be loop {loop_num + 1})")
            yield from self.start_loop(new_message= tool_results, model_id= model_id, message_type= MessageType.TOOL, conversation_history= self.messages)
        else:
            logger.info(f"  no tool calls — loop {loop_num} done")

        logger.info(f"{'='*40} END LOOP {loop_num} {'='*40}")
                    
                        
               
                        





           




