from dataclasses import dataclass
from typing import Any
from jemma.enums.response_enums import ResponseType

@dataclass
class AgentResponse:

    """
    Args
    
    type: The type of response, used to determine what type of UI widget to build
    content: User facing text to display within the appropriate widget
    
    
    """
    type: ResponseType
    content: Any
    model_feedback: str