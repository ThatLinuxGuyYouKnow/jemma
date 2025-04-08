import atexit
from configparser import Error
import signal
import sys
 
from requests.exceptions import RequestException
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import errorText, responseFormatter, warningText
def handle_exit(signum=None, frame=None):
    """Handle program exit with proper cleanup and status code"""
    
    print("\nExiting Jemma...")
    sys.exit(0 if signum in (signal.SIGINT, signal.SIGTERM) else 1)

# Register the exit handler
atexit.register(handle_exit)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
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
 
