import argparse
import atexit
import os
from pathlib import Path
import signal
import sys
from jemma.config import configure_jemma
from jemma.model.commandWatch import watchCommand
from jemma.model.editCode import editCode
from jemma.utils.getApiKey import get_api_key
from jemma.utils.getConfig import get_config
from jemma.utils.getFilesContent import get_files_content
from jemma.utils.terminalPrettifier import errorText, successText, warningText
from .utils.fileSpitter import spitAllFiles
from .model.explainCodebase import explainCode
from .model.startSession import startCodeSession



def main():
    try:
        parser = argparse.ArgumentParser(description="Get coding help right in your terminal!")
        parser.add_argument("-ex", "--explain", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
        parser.add_argument("-ch", "--chat", action="store_true", help="Start an interactive session, no access to codebase")
        parser.add_argument("-config", "--configure", action="store_true", help="Start your jemma experience, set preferences")
        parser.add_argument("-w", "--watch", nargs='+', help="Jemma will run this command watch the output for you")
        parser.add_argument("-ed", "--edit", type=str, nargs='+', help="Let Jemma help you fix bugs and add features")
        parser.add_argument("output", nargs="?", default="README.md", help="Output file path (default: README.md)")
        
        args = parser.parse_args()
        
        # Get API key and check if it exists
        apiKey: str = get_api_key()
        if not apiKey:
            print("You'll need to setup your api key first to use Jemma, Please run "+ successText('jemma-init'))
            return 1
        
        # Get directory structure and file contents
        path = os.getcwd()
        dc = os.listdir(path)
        ds = spitAllFiles(dc)
        content = get_files_content()
        
        # Process arguments
        if args.chat:
            print('Hallo!, lets get started!')
            firstPrompt = input('>')
            startCodeSession(firstPrompt)
        elif args.watch:
            commandToRun = "".join(args.watch)
            watchCommand(functionToRun=commandToRun, directoryStructure=ds, codeContent=content)
        elif args.configure:
            configure_jemma()
        elif args.explain:
            print(warningText('Parsing Codebase....'))
            explainCode(directoryStructure=ds, files=content)
        elif args.edit:
            user_prompt = ''.join(args.edit)
            print(warningText(user_prompt))
            editCode(directoryStructure=ds, fileContents=content, userPrompt=user_prompt)
        else:
            parser.print_help()
            
        return 0
        
    except Exception as e:
        print(errorText(f"An unexpected error occurred: {e}"))
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)