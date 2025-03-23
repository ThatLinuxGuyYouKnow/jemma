from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


def responseFormatter(text: str):
    """Add colors to different response sections"""
    # Color code patterns
    formatted = text.replace('**', Style.BRIGHT + Fore.YELLOW)  # Bold text
    formatted = formatted.replace('*', Fore.CYAN)              # Italics
    formatted = formatted.replace('`', Fore.GREEN)             # Code blocks
    
    # Section headers
    formatted = formatted.replace('Framework:', "\n" + Fore.MAGENTA + "Framework:")
    formatted = formatted.replace('Critical Logic:', "\n" + Fore.MAGENTA + "Critical Logic:")
    formatted = formatted.replace('Potential Issues:', "\n" + Fore.RED + "Potential Issues:")
    return formatted

def errorText(text: str):
    formatted = Style.BRIGHT + Fore.RED + text
    return formatted

def warningText(text: str):
    formatted = Style.BRIGHT + Fore.YELLOW + text
    return formatted

def successText(text: str):
    formatted = Style.BRIGHT + Fore.GREEN + text
    return formatted

def colouredText( text: str, colour: str, textStyle: str):
    formatted = Style.textStyle + Fore.colour + text
    return formatted