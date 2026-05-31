from litellm import completion
import os

def get_model_response(model_id: str, messages : list[str]) :

    for chunk in completion(
        model= model_id,
        messages=messages,
        stream=True
    ):
        
        yield chunk.choices[0].delta.content or ""





