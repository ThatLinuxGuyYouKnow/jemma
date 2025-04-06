import json
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.replaceFileContentByLines import replace_lines_in_file
from jemma.utils.terminalPrettifier import errorText, responseFormatter


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
        }},
           {{
           "isNewFile":"true"
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
    try:
      modelResponse: str = modelInteraction(prompt=prompt, isJsonResponse=True).strip('json')
      print(responseFormatter(modelResponse))
      processChanges(modelResponse=modelResponse)
     
    except Exception as e:  
        print(errorText(f'Something went wrong \n Please try again {e}'))
     


def processChanges(modelResponse: str):
    # Parse the JSON response
    response_data = json.loads(modelResponse)
    file_patches = response_data.get("changes", [])
    
    for patch in file_patches:
        start_line = patch['start_line']
        end_line = patch['end_line']
        file = patch['file']
        replacement = patch['replacement']
        
        # Convert list of replacement lines to a single string with newlines
        replacement_content = '\n'.join(replacement)
        
        # Apply the patch
        replace_lines_in_file(file, start_line=start_line, end_line=end_line, new_content=replacement_content)
    
    return len(file_patches)