import argparse
import os
from pathlib import Path

from jemma.initialization import initialize_jemma
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

def get_files_content(directory="."):
    """Get content of relevant files in the project."""
    ignored_dirs = {".git", "node_modules", "venv", "env", "build", "dist", "__pycache__","android","build","macos","ios","linux","web","test","windows"}
    ignored_extensions = {".pyc", ".pyo", ".pyd", ".so", ".dll", ".class", ".exe", ".obj", ".o",".h5",".csv"}
    
    all_content = ""
    
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if not any(file.endswith(ext) for ext in ignored_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        all_content += f"\n\nFile: {file_path}\n```\n{content}\n```\n"
                except:
                    # Skip files that can't be read as text
                    pass
    
    return all_content
def main():
     parser = argparse.ArgumentParser(description="Get coding help right in your terminal!")
     parser.add_argument("-e", "--explain", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
     parser.add_argument("-s", "--start", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
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

 