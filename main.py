import os
import subprocess
from colorama import init, Fore, Style

from core.board import create_board, update_board_state, get_board_data
from core.rules import arbiter
from core.utils import change_notations
from ui.renderer import print_board_high_res

# Initialize Colorama for Windows support
init()

def clear_screen():
    # Cross-platform clear
    _ = subprocess.run('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Start with the standard board
    current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    # Store last error message to display it once
    error_message = ""

    while True:
        clear_screen()
        
        # 2. Parse current state
        board = create_board(current_fen)
        board_data = get_board_data(current_fen)
        turn = board_data["turn"]
        turn_text = "WHITE" if turn == "w" else "BLACK"
        
        # 3. Render
        print_board_high_res(board)
        
        print(f"  Turn: {Style.BRIGHT}{turn_text}{Style.RESET_ALL}")
        if error_message:
            print(f"  {Fore.RED}Error: {error_message}{Style.RESET_ALL}")
            error_message = "" # Clear after showing
        
        # 4. Input
        try:
            user_input = input("\n  Enter Move (e.g. e2e4) or 'q' to quit: ").strip()
        except KeyboardInterrupt:
            print("\n  Game Exit.")
            sys.exit()

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("  Thanks for playing!")
            break
            
        # Basic Input Validation
        if len(user_input) != 4:
            error_message = "Invalid format. Use 4 chars like 'e2e4'."
            continue

        try:
            # 5. Coordinate Conversion
            # e2 -> (6, 4)
            start_str = user_input[0:2]
            end_str = user_input[2:4]
            
            start_pos = change_notations(start_str)
            end_pos = change_notations(end_str)
            
            # Check bounds just in case input was 'z9z9'
            if not (0 <= start_pos[0] < 8 and 0 <= start_pos[1] < 8):
                error_message = "Coordinates out of bounds."
                continue

            # 6. Rules Validation (The Arbiter)
            # Check 1: Is it the correct player's turn?
            piece_color = 'w' if turn == 'w' else 'b' # Assuming board functions return 'w'/'b'
            # Note: We need to verify the piece at start_pos belongs to current player
            # We can use our base logic, or just let arbiter return [] if wrong color.
            # But let's be explicit:
            
            # Get valid moves for the selected piece
            legal_moves = arbiter.get_legal_moves(board, start_pos)
            
            # Check 2: Is the move in the allowed list?
            if end_pos in legal_moves:
                # 7. Execute Move
                # This returns the NEW FEN string (with turn flipped)
                current_fen = update_board_state(user_input, current_fen)
            else:
                error_message = "Illegal move! (Checkmate? Pin? Blocked?)"
                
        except Exception as e:
            # Catch weird logic errors during dev so the app doesn't crash
            error_message = f"System Error: {e}"
            # For debugging, you might want to print(e) directly or remove this try/except block
            # raise e 

if __name__ == "__main__":
    main()
