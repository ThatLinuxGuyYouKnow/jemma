from jemma.model.modelInteraction import modelInteraction
from jemma.utils.replaceFileContentByLines import replace_lines_in_file
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
          "file": "tools/main.py",
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
    print(responseFormatter(modelResponse))


def processChanges(filePatches: str):
    number_of_patches = 0
    for patch in filePatches and number_of_patches < len(filePatches) and number_of_patches + 1 :
        start_line: str = filePatches[number_of_patches]['start_line']
        end_line: str = filePatches[number_of_patches]['start_line']
        file: str = filePatches[number_of_patches]['file']
        replacement: str = filePatches[number_of_patches]['replacement']
        replace_lines_in_file(file, start_line=start_line, end_line=end_line, new_content=replacement)
    