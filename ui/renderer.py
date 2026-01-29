import os
import shutil
from colorama import Fore, Back, Style

# --- CONFIGURATION ---
COLOR_LIGHT_SQ = Back.LIGHTBLACK_EX
COLOR_DARK_SQ = Back.CYAN
COLOR_HIGHLIGHT_MOVE = Back.GREEN
COLOR_HIGHLIGHT_ERROR = Back.RED
COLOR_HIGHLIGHT_SRC = Back.YELLOW
COLOR_HIGHLIGHT_LAST_MOVE = Back.MAGENTA # Purple for last move

COLOR_WHITE_P = Fore.WHITE + Style.BRIGHT
COLOR_BLACK_P = Fore.BLACK

# WINDOWS SAFE MODE: Use Letters by default.
USE_ICONS = False 

ICONS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    '+': ' ' 
}

LETTERS = {
    'r': 'R', 'n': 'N', 'b': 'B', 'q': 'Q', 'k': 'K', 'p': 'P',
    'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P',
    '+': ' '
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_graveyard(board):
    initial = {
        'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1,
        'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1
    }
    current = {}
    for row in board:
        for char in row:
            if char != "+":
                current[char] = current.get(char, 0) + 1
    
    graveyard = {'w': [], 'b': []}
    symbols = ICONS if USE_ICONS else LETTERS
    
    for piece, count in initial.items():
        diff = count - current.get(piece, 0)
        if diff > 0:
            color = 'w' if piece.isupper() else 'b'
            graveyard[color].extend([symbols[piece]] * diff)
            
    return graveyard

def generate_board_lines(board, highlights=None, error_pos=None, check_pos=None, last_move=None):
    if highlights is None: highlights = []
    if last_move is None: last_move = []
    
    lines = []
    symbols = ICONS if USE_ICONS else LETTERS
    
    # Header (File Labels)
    gap = " " * 6
    header = "        " + gap.join("ABCDEFGH") + "   "
    lines.append(header)
    
    for r in range(8):
        # 3 lines per Rank
        line_top = f"     "   # Padding
        line_mid = f"  {8-r}  " # Rank Label
        line_bot = f"     "   # Padding
        
        for c in range(8):
            piece_char = board[r][c]
            
            # Priority Color Logic
            if check_pos == (r, c): 
                bg = COLOR_HIGHLIGHT_ERROR
            elif error_pos == (r, c): 
                bg = COLOR_HIGHLIGHT_ERROR
            elif (r, c) in highlights: 
                bg = COLOR_HIGHLIGHT_MOVE
            elif (r, c) in last_move:
                bg = COLOR_HIGHLIGHT_LAST_MOVE
            else:
                bg = COLOR_LIGHT_SQ if (r + c) % 2 == 0 else COLOR_DARK_SQ
            
            # Foreground Color
            if piece_char == "+": fg = ""
            elif piece_char.isupper(): fg = COLOR_WHITE_P
            else: fg = COLOR_BLACK_P
            
            symbol = symbols.get(piece_char, ' ')
            
            # Construct Tile (7 chars wide)
            padding = "   "
            
            # 1. Top
            line_top += f"{bg}{padding} {padding}{Style.RESET_ALL}"
            # 2. Middle
            line_mid += f"{bg}{padding}{fg}{symbol}{padding}{Style.RESET_ALL}"
            # 3. Bottom
            line_bot += f"{bg}{padding} {padding}{Style.RESET_ALL}"
            
        lines.append(line_top)
        lines.append(line_mid)
        lines.append(line_bot)
        
    lines.append(header)
    return lines

def draw_game_state(board, turn, game_status="PLAYING", highlights=None, error_pos=None, check_pos=None, last_move=None, message=""):
    clear_screen()
    board_lines = generate_board_lines(board, highlights, error_pos, check_pos, last_move)
    graveyard = get_graveyard(board)
    
    # Stats Panel
    stats = []
    stats.append(f"{Style.BRIGHT}:: TCHESS ENGINE ::{Style.RESET_ALL}")
    stats.append("")
    stats.append(f"Turn:   {'WHITE' if turn == 'w' else 'BLACK'}")
    stats.append(f"Status: {game_status}")
    stats.append("")
    stats.append("Captured:")
    stats.append(f" [W]: {' '.join(graveyard['w'])}")
    stats.append(f" [B]: {' '.join(graveyard['b'])}")
    stats.append("")
    
    if message:
        stats.append(f"{Fore.YELLOW}INFO:{Style.RESET_ALL}")
        # Manual Wrap
        words = message.split()
        line = ""
        for w in words:
            if len(line) + len(w) > 25:
                stats.append(line)
                line = w + " "
            else:
                line += w + " "
        stats.append(line)

    # Stitching
    max_lines = max(len(board_lines), len(stats))
    
    term_width = shutil.get_terminal_size().columns
    term_height = shutil.get_terminal_size().lines
    
    # Visual width estimation (Board ~65 chars + Gap 4 + Stats ~30)
    total_content_width = 99
    
    padding_left = " " * max(0, (term_width - total_content_width) // 2)
    padding_top = max(0, (term_height - max_lines - 3) // 2)
    
    print("\n" * padding_top)
    
    for i in range(max_lines):
        if i < len(board_lines):
            b_line = board_lines[i]
        else:
            b_line = " " * 65 # Pad if board is shorter than stats (unlikely)
            
        s_line = stats[i] if i < len(stats) else ""
        
        gap = "    "
        print(f"{padding_left}{b_line}{gap}{s_line}")

    print("\n")

def get_player_input(turn_color):
    prompt_char = "❯"
    color = Fore.GREEN if turn_color == 'w' else Fore.BLUE
    try:
        return input(f" {color}[{'WHITE' if turn_color == 'w' else 'BLACK'}] {prompt_char}{Style.RESET_ALL} ").strip()
    except KeyboardInterrupt:
        return "q"
