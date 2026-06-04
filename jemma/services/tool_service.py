import json
import inspect
from jemma.tools.registry import TOOL_FUNCTIONS
 
from jemma.exceptions.tool_call_exceptions import ToolCallException, InvalidToolArguments
from jemma.validators.tool_call_validators import validate_tool_exists

class ToolOrchestrator():

    def __init__(self):

        self.registry = TOOL_FUNCTIONS


    def execute_tool_calls(self, accumulated_tool_calls: dict):

        tool_call_results  = []

        for tool_call in accumulated_tool_calls.values():

            func_name = tool_call["name"]
            tool_call_id = tool_call["id"]
            args_string = tool_call["arguments"]

            if not validate_tool_exists(tool_name= func_name, tool_registry= self.registry):

                raise ToolCallException(model_error_feedback= "This tool does not exist, try again with a valid tool")
            
            try:

                kwargs = json.loads(args_string) if args_string else {}

            except json.JSONDecodeError:

                raise InvalidToolArguments(model_error_feedback= "Invalid arguments provided for this tool, try again with valid arguments")
            
            func = self.registry[func_name]

            result = func(**kwargs)

            """To ensure our result is always a text response"""

            result_str: str = result if isinstance(result, str) else json.dumps(result)


            tool_call_results.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": func_name,
                "tool_result": result_str
            })

        return tool_call_results



                

            




