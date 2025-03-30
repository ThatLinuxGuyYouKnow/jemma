import os
import subprocess

from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import responseFormatter


def watchCommand(functionToRun: str, directoryStructure: str, codeContent: str):
   print(functionToRun)
   result = subprocess.run(
                functionToRun.strip(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
  
   model_prompt = f"""
        Analyze this command execution context:
        Codebase Structure: {directoryStructure}
        Code Content: {codeContent}
        Executed Command: {functionToRun}
        Command Output: {result.stdout}
        Exit Code: {result.returncode}
        
        Provide concise user-facing analysis of potential issues and suggestions.
        """
   model_response = responseFormatter( modelInteraction(model_prompt))
   print(model_response)