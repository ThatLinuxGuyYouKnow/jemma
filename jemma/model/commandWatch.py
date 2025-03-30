import os
import subprocess

from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import responseFormatter


def watchCommand(functionToRun, directoryStructure: str, codeContent: str):
   print(functionToRun)
   result = subprocess.run(
                functionToRun.split(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
   command_result = result.stdout
   model_prompt=f""" You are to return a response based on the codebase and resulting terminal output, your response should be user facing
   code content: ${codeContent}
   Directory Structure: ${directoryStructure}
   Terminal Output: ${command_result}"""
   model_response = responseFormatter( modelInteraction(model_prompt))
   print(model_response)