from ..utils.terminalPrettifier import jemmaText, successText, errorText, warningText

def display_header():
    """Displays the Jemma CLI header."""
    # ASCII Art for Jemma - inspired by Gemini CLI
    logo = r"""
    ██╗███████╗███╗   ███╗███╗   ███╗ █████╗ 
    ██║██╔════╝████╗ ████║████╗ ████║██╔══██╗
    ██║█████╗  ██╔████╔██║██╔████╔██║███████║
    ██║██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║
    ██║███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║
    ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    """

    lines = logo.split('\n')
    for line in lines:
        print(jemmaText(line))

    print(successText("Tips for getting started:"))
    print("1. Ask questions, edit files, or run commands.")
    print("2. Be specific for the best results.")
    print("3. Create JEMMA.md files to customize your interactions with Jemma.")
    print("4. /help for more information.")
    print("\n")

def get_user_input():
    """Gets user input with a styled prompt."""
    prompt = f"{jemmaText('>')} Type your message or @path/to/file\n"
    return input(prompt)
