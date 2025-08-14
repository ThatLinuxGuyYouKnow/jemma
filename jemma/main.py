# jemma/main.py (or your main entrypoint file)

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
from jemma.utils.getFilesContent import get_files_content
from jemma.utils.terminalPrettifier import errorText, successText, warningText
from .utils.fileSpitter import spitAllFiles
from .model.explainCodebase import explainCode
from .model.startSession import chat_loop

# Global cleanup state
_cleanup_done = False

def cleanup():
    """Global cleanup handler (runs only once)"""
    global _cleanup_done
    if _cleanup_done:
        return

    _cleanup_done = True
    chat_file = Path('.current_chat.txt')
    try:
        if chat_file.exists():
            chat_file.unlink()
            print(successText("\n✅ Cleaned up chat history"))
    except Exception as e:
        pass

def handle_exit(signum=None, frame=None):
    """Unified exit handler"""
    print(warningText('\nExiting Jemma gracefully'))
    cleanup()
    sys.exit(0)

if not hasattr(sys, 'cleanup_registered'):
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    sys.cleanup_registered = True

def main():
    try:
        parser = argparse.ArgumentParser(description="Get coding help right in your terminal!")

 
        parser.add_argument(
            "-ch", "--chat",
            nargs='*',   
            help="Start an interactive session. Optionally provide an initial prompt after the flag."
        )
        # ----------------------------------

        parser.add_argument("-ex", "--explain", action="store_true", help="Explain this repository, provide an overview of critical functions and/or views")
        parser.add_argument("-config", "--configure", action="store_true", help="Start your jemma experience, set preferences")
        parser.add_argument("-w", "--watch", nargs='+', help="Jemma will run this command watch the output for you")
        parser.add_argument("-ed", "--edit", type=str, nargs='+', help="Let Jemma help you fix bugs and add features")
        parser.add_argument("output", nargs="?", default="README.md", help="Output file path (default: README.md)")

        args = parser.parse_args()

        apiKey: str = get_api_key()
        if not apiKey:
            print("You'll need to setup your api key first to use Jemma, Please run "+ successText('jemma-init'))
            return 1

        if args.chat is not None:
            # This correctly joins arguments into a single string
            initial_prompt = " ".join(args.chat) 
            
            # This one call is all you need. It will handle the rest.
            chat_loop(initial_prompt=initial_prompt) 
            return 0

        # path = os.getcwd()
        #dc = os.listdir(path)
        # ds = spitAllFiles(dc)
        # content = get_files_content()

        if args.watch:
            commandToRun = "".join(args.watch)
            watchCommand(functionToRun=commandToRun, directoryStructure=ds, codeContent=content)
        elif args.configure:
            configure_jemma()
        elif args.explain:
            print(warningText('Parsing Codebase....'))
            explainCode(directoryStructure=ds, files=content)
        elif args.edit:
            user_prompt = ''.join(args.edit)
            editCode(directoryStructure=ds, fileContents=content, userPrompt=user_prompt)
        else:
            parser.print_help()

        return 0

    except Exception as e:
 
        print(errorText(f"An unexpected error occurred: {e}"))
        return 1

if __name__ == "__main__":
    sys.exit(main())