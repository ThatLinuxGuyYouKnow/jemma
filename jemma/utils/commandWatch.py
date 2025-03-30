import os
import subprocess

from jemma.model.modelInteraction import modelInteraction


def watchCommand(functionToRun, directoryStructure: str, codeContent: str):
   result = subprocess.run(
                functionToRun.split(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
   command_result = result.stdout
   model_prompt=f""" You are to return a response based on the codebase and resulting terminal output 
   code content: ${codeContent}
   Directory Structure: ${directoryStructure}
   Terminal Output: ${command_result}"""
   modelInteraction(prompt="")
            print(f"\nCommand output:\n{result.stdout}")