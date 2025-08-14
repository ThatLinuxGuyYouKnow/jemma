 

import os
import sys
from pathlib import Path

from jemma.config import JemmaConfig
from jemma.model import modelInteraction
from jemma.utils.terminalPrettifier import errorText, successText, warningText
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
    print("Type your message and press Enter. Use '/exit', Ctrl+C, or Ctrl+D to quit.\n")

def process_turn(user_prompt: str):
    """
    Handles a single turn of the conversation: reads history, gets model
    response, and updates history.
    """
    history = ""
    # Ensure history file exists before trying to read
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = f.read()

    print(warningText("Jemma is thinking..."))
    full_prompt = history + f"USER: {user_prompt}\n"
    model_response = modelInteraction(full_prompt)

    if model_response:
        # Use a more visually distinct separator for assistant's response
        print(f"\n{successText('ASSISTANT:')}\n{model_response}\n" + "-"*40)
        with open(CHAT_HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f'USER: {user_prompt}\n\n')
            f.write(f'ASSISTANT: {model_response}\n\n')
    else:
        print(errorText("Jemma could not provide a response."))

def chat_loop(initial_prompt: str = ""):
    """
    The main chat loop. It can optionally process an initial prompt
    before starting the interactive session.
    """
    # Ensure the chat history is clean for a new session
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)

    input_history = FileHistory('.jemma_cli_input_history.txt')
    session = PromptSession(history=input_history)

    style = Style.from_dict({
        'prompt': 'ansicyan bold',
        'placeholder': 'ansigray',
        'toolbar': 'bg:#222222 #ffffff',
    })

    bottom_toolbar = FormattedText(
        [('class:toolbar', f" {CONFIG.model} (temp: {CONFIG.temperature}) ")],
        style='class:toolbar'
    )

    print_logo()

    # --- KEY CHANGE: HANDLE INITIAL PROMPT ---
    # If an initial prompt is provided, process it first.
    if initial_prompt:
        print(f"Processing initial request: \"{initial_prompt}\"")
        process_turn(initial_prompt)

    # --- KEY CHANGE: THE ACTUAL LOOP ---
    # Start the interactive loop for subsequent messages.
    while True:
        try:
            user_prompt = session.prompt(
                '> ',
                style=style,
                placeholder='Type your message...',
                bottom_toolbar=bottom_toolbar,
                rprompt=f"{Path(os.getcwd()).name}",
            )

            # Check for exit command
            if user_prompt.lower().strip() == '/exit':
                break

            # If user just hits enter, continue to the next prompt
            if not user_prompt.strip():
                continue

            # Process the turn with the new user input
            process_turn(user_prompt)

        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C (KeyboardInterrupt) and Ctrl+D (EOFError)
            break

    # The cleanup function registered with atexit will handle the file deletion.
    # We just need to print a friendly message.
    print(warningText("\nChat session ended."))