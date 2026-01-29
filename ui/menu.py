import os
from colorama import Fore, Style, init

init()

LOGO = r"""
████████  ██████ ██   ██ ███████ ███████ ███████ 
   ██    ██      ██   ██ ██      ██      ██      
   ██    ██      ███████ █████   ███████ ███████ 
   ██    ██      ██   ██ ██           ██      ██ 
   ██     ██████ ██   ██ ███████ ███████ ███████ 
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    """
    Returns a dict: {'mode': 'pvp'|'pve', 'difficulty': 1-4, 'color': 'w'|'b'}
    """
    while True:
        clear_screen()
        print(Fore.CYAN + LOGO + Style.RESET_ALL)
        print("    " + "="*40)
        print(f"    {Style.BRIGHT}WELCOME TO TCHESS{Style.RESET_ALL}")
        print("    " + "="*40 + "\n")
        
        print("    [1] Player vs Player (Local)")
        print("    [2] Player vs CPU (Easy)")
        print("    [3] Player vs CPU (Medium)")
        print("    [4] Player vs CPU (Hard)")
        print("    [5] Player vs CPU (Grandmaster)")
        print("\n    [Q] Quit")
        
        choice = input("\n    Select Mode ❯ ").strip().lower()
        
        # Default config
        config = {'mode': 'pve', 'difficulty': 1, 'color': 'w'}

        if choice == '1':
            return {'mode': 'pvp', 'difficulty': 0, 'color': 'w'}
        
        elif choice == 'q':
            exit()
            
        elif choice in ['2', '3', '4', '5']:
            # Map choice to difficulty
            diff_map = {'2': 1, '3': 2, '4': 3, '5': 4}
            config['difficulty'] = diff_map[choice]
            
            # Ask for Color in PVE
            print("\n    " + "-"*20)
            print("    [W] Play as White (First)")
            print("    [B] Play as Black (Second)")
            c_choice = input("\n    Select Color ❯ ").strip().lower()
            
            config['color'] = 'b' if c_choice == 'b' else 'w'
            return config
