from colorama import Fore, Back, Style

# Map internal chars to Unicode Chess Symbols
SYMBOLS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    '+': ' ' 
}

def print_board_high_res(board: list[list[str]]) -> None:
    """
    Prints the board to terminal using ANSI colors and Unicode symbols.
    """
    print("\n")
    print("    " + "  ".join("ABCDEFGH")) 
    
    for rank_idx in range(8):
        rank_num = 8 - rank_idx
        line = f" {rank_num} "
        
        for col_idx in range(8):
            piece_char = board[rank_idx][col_idx]
            
            # 1. Background Logic
            # Even sum = Light Square, Odd sum = Dark Square
            if (rank_idx + col_idx) % 2 == 0:
                bg = Back.LIGHTCYAN_EX 
            else:
                bg = Back.LIGHTBLACK_EX 
            
            # 2. Piece Color Logic
            if piece_char != '+':
                if piece_char.isupper():
                    # White Piece: Bright White text
                    fg = Fore.WHITE + Style.BRIGHT
                else:
                    # Black Piece: Black text
                    fg = Fore.BLACK
            else:
                fg = "" # No color for empty space

            symbol = SYMBOLS.get(piece_char, ' ')
            
            # 3. Construct Tile
            # Reset style after every tile to prevent bleeding
            tile_str = f"{bg}{fg} {symbol} {Style.RESET_ALL}"
            line += tile_str
            
        print(line + f" {rank_num}")
        
    print("    " + "  ".join("ABCDEFGH"))
    print("\n")
