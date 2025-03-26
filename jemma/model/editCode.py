from jemma.model.modelInteraction import modelInteraction


def editCode(directoryStructure: str, fileContents: str, apiKey: str):
    prompt: str = {"Return fixes or feature additions based on the users request, return the code as code patches"
    "-Send the code in the format"
    "- 'start_line': int, the line number (1-indexed) where the change begins."
    "- 'end_line': int, the line number where the change ends (inclusive)"
    "- 'replacement': list of str, new lines to replace the specified range."
    "For example {'start_line':'46', 'end_line':'47', 'replacement':'print('Hello Gemini')}"}
    modelResponse: str = modelInteraction()
