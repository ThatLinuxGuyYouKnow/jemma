from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


def responseFormatter(text: str):
    formattedText =  text.replace('**',Style.BRIGHT + Fore.YELLOW)