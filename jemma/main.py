import argparse
import os
from pathlib import Path

from jemma.initialization import initialize_jemma
from jemma.utils.getApiKey import get_api_key
from jemma.utils.getFilesContent import get_files_content
from jemma.utils.terminalPrettifier import successText
from .utils.fileSpitter import spitAllFiles
from .model.explainCodebase import explainCode
from .model.startSession import startCodeSession

def main():
     parser = argparse.ArgumentParser(description="Get coding help right in your terminal!")
     parser.add_argument("-e", "--explain", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
     parser.add_argument("-ch", "--chat", action="store_true", help="Start an interactive session, no access to codebase")
     parser.add_argument("-init", "--initialize", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
     parser.add_argument("output", nargs="?", default="README.md", help="Output file path (default: README.md)")
     content = get_files_content()
     args = parser.parse_args()
     apiKey: str = get_api_key()
     if not apiKey:
            print("You'll need to setup your api key first to use jemma, Please run "+ successText('jemma-configure'))
     if args.chat:
         print('Hallo!, lets get started!')
         firstPrompt = input('>')
         startCodeSession(firstPrompt)
     if args.initialize:

         initialize_jemma()
     if args.explain:
     
      print('Parsing Codebase....')
      path = os.getcwd() 
      dc = os.listdir(path)
   
      ds = spitAllFiles(dc)
      explainCode(directoryStructure=ds,apikey=apiKey, files=content  )

 