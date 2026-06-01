from litellm import completion
from jemma.tools.registry import TOOL_SCHEMAS
import os

def get_model_response(model_id: str, messages : list[str]) :

    stream = completion(
        model= model_id,
        messages=messages,
        stream=True,
        tools = TOOL_SCHEMAS
    )

    for chunk in stream:

        delta = chunk.choices[0].delta

        yield delta

        




            





