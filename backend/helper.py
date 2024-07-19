from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_colored(text, color):
    color_dict = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    
    # Get the color from the dictionary
    color_code = color_dict.get(color.lower(), Fore.WHITE)
    
    # Print the text in the specified color
    print(color_code + text + Style.RESET_ALL)

