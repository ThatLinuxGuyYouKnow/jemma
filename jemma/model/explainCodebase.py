from configparser import Error
 
from requests.exceptions import RequestException
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import errorText, responseFormatter, warningText

def explainCode(directoryStructure: str, files: str):
 try :
    if not directoryStructure or not files:
        print(errorText('somethings wrong here'))
        quit()
    model_prompt = f"""Explain the following codebase, mentioning frameworks, languages, critical operating logic, and  only if you find any, critical bugs' 
    - Director Structure := ${directoryStructure}
    - File Content :=  ${files}"""
 
    response= modelInteraction(model_prompt)
    if response == None:
       print(errorText('Something went wrong \n Please try again'))
    print(responseFormatter(response))
 except Exception as e:
  print(errorText('An error occured '+ str(e)))
 
