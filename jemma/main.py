import argparse
import os
from pathlib import Path

from jemma.initialization import initialize_jemma
from jemma.utils.getFilesContent import get_files_content
from .utils.fileSpitter import spitAllFiles
from .model.explainCodebase import explainCode
from .model.startSession import startCodeSession
def get_api_key():
    # First check environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # If not in environment, check config file
    if not api_key:
        config_path = Path.home() / ".autodoc" / "config"
        if config_path.exists():
            with open(config_path, "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=")[1].strip()
    
    return api_key


def main():
     parser = argparse.ArgumentParser(description="Get coding help right in your terminal!")
     parser.add_argument("-e", "--explain", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
     parser.add_argument("-s", "--start", action="store_true", help="Start an interactive session, no access to codebase")
     parser.add_argument("-init", "--initialize", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
     parser.add_argument("output", nargs="?", default="README.md", help="Output file path (default: README.md)")
     content = get_files_content()
     args = parser.parse_args()
     if args.start:
         print('Alright lets get started!')
         firstPrompt = input('>')
         startCodeSession(firstPrompt)
     if args.initialize:
         if not get_api_key():
             print("You'll need to setup your api key first")
         initialize_jemma()
     if args.explain:
      if not get_api_key():
          print('Please run jemma-configure to set up your api key')
     
      print('Parsing Codebase....')
      files = get_files_content()
       
      path = os.getcwd() 
      dc = os.listdir(path)
   
      ds = spitAllFiles(dc)
      explainCode(directoryStructure=ds,apikey=get_api_key(), files=content  )

 