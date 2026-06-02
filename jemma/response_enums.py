from enum import Enum

class ResponseType(Enum):

    TEXT = "text"
    ERROR = "error" 
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


