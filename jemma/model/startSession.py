 
import os
from .modelInteraction import modelInteraction
from ..utils.terminalPrettifier import jemmaText, successText, errorText, warningText

from ..UI.display import display_header, get_user_input
def chat_loop(initial_prompt: str = ""):
    """
    Starts and manages a self-contained, interactive chat session with a Gemini-like interface.

    This function handles the entire lifecycle of a chat:
    - Displays the header.
    - Initializes a clean chat history file.
    - Processes an optional initial prompt.
    - Enters a robust loop for continuous conversation.
    - Allows the user to exit gracefully with 'exit' or 'quit'.

    Args:
        initial_prompt (str, optional): The first prompt to start the session with.
                                        If empty, the user will be prompted immediately.
    """
    chat_history_file = '.current_chat.txt'
    display_header()

    # Start with a clean slate for the new session.
    with open(chat_history_file, "w") as f:
        pass

    current_prompt = initial_prompt

    try:
        while True:
            if not current_prompt:
                current_prompt = get_user_input()

            if current_prompt is None:  # Handles Ctrl+D (EOFError)
                print(warningText("\nExiting..."))
                break

            # Check for exit command
            if current_prompt.lower().strip() in ['exit', 'quit']:
                print(warningText("Ending chat session."))
                break

            # Read the entire chat history for context
            try:
                with open(chat_history_file, 'r') as f:
                    chat_history = f.read()
            except FileNotFoundError:
                chat_history = ""

            # The model needs the full context
            full_prompt_for_model = chat_history + "USER: " + current_prompt
            
            # --- Interaction Logic ---
            model_response = modelInteraction(full_prompt_for_model)
            
            if model_response:
                print(jemmaText('Jemma :') + model_response)

                with open(chat_history_file, 'a') as f:
                    f.write(f"USER: {current_prompt}\n")
                    f.write(f"YOU(MODEL): {model_response}\n")
            else:
                print(errorText("Sorry, I couldn't generate a response. Please try again."))

            # Reset prompt for the next loop iteration to wait for user input
            current_prompt = ""

    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as e:
        print(errorText(f'\nAn error occurred during the chat: {str(e)}'))