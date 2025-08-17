 
import os
from .modelInteraction import modelInteraction
from ..utils.terminalPrettifier import jemmaText, successText, errorText, warningText

def chat_loop(initial_prompt: str = ""):
    """
    Starts and manages a self-contained, interactive chat session.

    This function handles the entire lifecycle of a chat:
    - Initializes a clean chat history file.
    - Processes an optional initial prompt.
    - Enters a robust loop (not recursion) for continuous conversation.
    - Allows the user to exit gracefully with 'exit' or 'quit'.
    - Relies on the main application's exit handlers for cleanup (Ctrl+C).

    Args:
        initial_prompt (str, optional): The first prompt to start the session with.
                                        If empty, the user will be prompted immediately.
    """
    chat_history_file = '.current_chat.txt'
    
    print(successText("Starting chat session. Type 'exit' or 'quit' to end."))

    # If an initial prompt was passed from the command line, print it for clarity
    if initial_prompt:
        print(f"> {initial_prompt}")

    # Start with a clean slate for the new session.
    # The atexit handler in main.py will remove this file on final exit.
    with open(chat_history_file, "w") as f:
        # Just creating/truncating the file is enough
        pass

    current_prompt = initial_prompt

    try:
        while True:
            # If not the first turn, or if no initial prompt was given, get input.
            if not current_prompt:
                current_prompt = input('> ')

            # Check for exit command
            if current_prompt.lower().strip() in ['exit', 'quit']:
                print(warningText("Ending chat session."))
                break # Exit the loop gracefully

            # Read the entire chat history for context
            try:
                with open(chat_history_file, 'r') as f:
                    chat_history = f.read()
            except FileNotFoundError:
                chat_history = "" # Should not happen, but safe to handle

            # The model needs the full context
            full_prompt_for_model = chat_history + "USER: " + current_prompt
            
            # --- Interaction Logic ---
            model_response = modelInteraction(full_prompt_for_model)
            
            if model_response:
                # Print the response for the user
                print(jemmaText('Jemma :') + model_response) # Assuming modelInteraction formats its output

                # Update the history file for the next turn
                with open(chat_history_file, 'a') as f:
                    f.write(f"USER: {current_prompt}\n")
                    f.write(f"YOU(MODEL): {model_response}\n")
            else:
                print(errorText("Sorry, I couldn't generate a response. Please try again."))

            # Reset prompt for the next loop iteration to wait for user input
            current_prompt = ""

    except (KeyboardInterrupt, EOFError):
        # A KeyboardInterrupt (Ctrl+C) or EOFError (Ctrl+D) will break the loop.
        # The main.py signal handler will then print the exit message and clean up.
        pass
    except Exception as e:
        print(errorText(f'\nAn error occurred during the chat: {str(e)}'))
        # The session ends, and the main cleanup will still run.