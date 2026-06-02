from enum import Enum

class MessageType(Enum):

    USER:str = 'user'
    TOOL :str= 'tool'
    SYSTEM:str = 'system'
    ASSISTANT: str = 'assistant'