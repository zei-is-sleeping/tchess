from colorama import Fore, Back, Style

SYMBOLS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    '+': ' ' 
}

def print_board_high_res(board):
    print("\n")
    print("    " + "  ".join("ABCDEFGH")) 
    
    for rank_idx in range(8):
        rank_num = 8 - rank_idx
        line = f" {rank_num} "
        
        for col_idx in range(8):
            piece_char = board[rank_idx][col_idx]
            
            # 1. Background Logic
            # Blue is great for dark squares. 
            # For light squares, standard White (Back.WHITE) is very bright.
            # Try Back.LIGHTBLACK_EX (Dark Grey) for a "Dark Mode" board, 
            # or keep Back.WHITE if you like the classic look.
            if (rank_idx + col_idx) % 2 == 0:
                bg = Back.LIGHTCYAN_EX 
            else:
                bg = Back.LIGHTBLACK_EX 
            
            # 2. Piece Color Logic
            if piece_char != '+':
                if piece_char.isupper():
                    # White Piece: Bright White text
                    # If background is White, we need a shadow or something?
                    # Actually, White Text on White BG is invisible.
                    # CRUCIAL DECISION: 
                    # If BG is WHITE, White pieces must be BLACK (or dark grey) text to show up?
                    # BUT that confuses them with Black pieces.
                    
                    # BETTER APPROACH: 
                    # Change the Light Square color to Dark Grey (Back.BLACK + Style.BRIGHT -> Dark Grey)
                    # So White pieces (Fore.WHITE) pop against it.
                    
                    # Let's try: White Pieces = Fore.WHITE + Style.BRIGHT (Glowing White)
                    fg = Fore.WHITE + Style.BRIGHT
                else:
                    # Black Piece: Black text
                    # On Blue BG, Black text is okay.
                    fg = Fore.BLACK
            else:
                fg = ""

            symbol = SYMBOLS.get(piece_char, ' ')
            
            # 3. Construct Tile
            # reset style after every tile to prevent bleeding
            tile_str = f"{bg}{fg} {symbol} {Style.RESET_ALL}"
            line += tile_str
            
        print(line + f" {rank_num}")
        
    print("    " + "  ".join("ABCDEFGH"))
    print("\n")
