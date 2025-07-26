import os
import signal
import sys
import json
from pathlib import Path
from typing import Dict, Any

# --- Prompt Toolkit Imports ---
from jemma.config import JemmaConfig
from jemma.model import modelInteraction
from jemma.utils.terminalPrettifier import errorText, successText
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText

 
CONFIG = JemmaConfig()
CHAT_HISTORY_FILE = '.current_chat.txt'

 

def print_logo():
    """Prints a cool ASCII art logo."""
    logo = """
██████╗ ███████╗███╗   ███╗███╗   ███╗ █████╗ 
██╔══██╗██╔════╝████╗ ████║████╗ ████║██╔══██╗
██████╔╝█████╗  ██╔████╔██║██╔████╔██║███████║
██╔══██╗██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║
██║  ██║███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    """
    print(successText(logo))
    print("Welcome to the Jemma CLI!")
    print("Type your message and press Enter. Use '/exit' or Ctrl+C to quit.\n")

def chat_loop(initial_prompt: str = ""):
    """
    The main chat loop integrating your logic with the advanced UI.
    """
  
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)
        
   
    input_history = FileHistory('.jemma_cli_input_history.txt')
    session = PromptSession(history=input_history)

    # UI Styling
    style = Style.from_dict({
        'prompt': 'ansicyan bold',
        'placeholder': 'ansigray',
        'toolbar': 'bg:#222222 #ffffff',
    })

     
    bottom_toolbar = FormattedText(
        [('class:toolbar', f" {CONFIG.model} (temp: {CONFIG.temperature}) ")],
        style='class:toolbar'
    )
    
    def process_turn(user_prompt):
        """Handles a single turn of the conversation."""
         
        history = ""
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = f.read()
        
     
        full_prompt = history + f"USER: {user_prompt}\n"
        model_response = modelInteraction(full_prompt)
        
        if model_response:
        
            print(f"\n{successText('ASSISTANT:')}\n{model_response}\n")
            with open(CHAT_HISTORY_FILE, 'a', encoding='utf-8') as f:
                f.write(f'USER: {user_prompt}\n\n')
                f.write(f'YOU(MODEL): {model_response}\n\n')

   
    if initial_prompt:
        print(f"Starting session with initial prompt: '{initial_prompt}'")
        process_turn(initial_prompt)
        user_prompt = session.prompt(
                '> ', 
                style=style,
                placeholder='Type your message...',
                bottom_toolbar=bottom_toolbar,
            )

        if user_prompt.lower().strip() == '/exit':
                raise KeyboardInterrupt

    else:
        process_turn(user_prompt)

       
 
    
 
