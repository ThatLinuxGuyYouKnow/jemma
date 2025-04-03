from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import responseFormatter


def editCode(directoryStructure: str, fileContents: str,  userPrompt:str):
    prompt = f"""Return fixes or feature additions based on the users request, return the code as code patches"
    "-Send the code in the format"
    "- 'start_line': int, the line number (1-indexed) where the change begins."
    "- 'end_line': int, the line number where the change ends (inclusive)"
    "- 'replacement': list of str, new lines to replace the specified range."
    "For example     {{
      "changes": [
        {{
          "file": "absolute_path/main.py",
          "start_line": 46,
          "end_line": 47,
          "replacement": ["print('Hello Jemma')"]
        }}
      ],
      "narration": "Updated print statement to fix output"
    }}
    Using the preceeding instruction, operate on this codebase
    "Here is the users request :={userPrompt}
    "Here is the projects directory structure :={directoryStructure}"
    "Here is the file content := {fileContents}
     Remember to return *ONLY* json"""
    modelResponse: str = modelInteraction(prompt=prompt).strip('json')
    print(responseFormatter(modelResponse["narration"]))
