from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import responseFormatter


def editCode(directoryStructure: str, fileContents: str, apiKey: str):
    prompt: str = {"Return fixes or feature additions based on the users request, return the code as code patches"
    "-Send the code in the format"
    "- 'start_line': int, the line number (1-indexed) where the change begins."
    "- 'end_line': int, the line number where the change ends (inclusive)"
    "- 'replacement': list of str, new lines to replace the specified range."
    "For example {'changes':{'file' :'absolute_file_path.py','start_line':'46', 'end_line':'47', 'replacement':'print('Hello Gemini')}, {'file' :'second_file_path.py','start_line':'12', 'end_line':'15', 'replacement':'print('Hello User')}, 'narration' : 'The files changed file and changed file 2 were changed to avoid forever loops }"
    "Using the preceeding instruction, operate on this codebase"
    f"Here is the projects directory structure :={directoryStructure}"
    f"Here is the file content := {fileContents}"}
    modelResponse: str = modelInteraction(prompt=prompt)
    print(responseFormatter(modelResponse))
