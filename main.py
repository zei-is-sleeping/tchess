from colorama import init

# Core
from core.board import create_board, update_board_state, get_board_data
from core.rules import arbiter
from core.utils import change_notations
from core import storage, ai

# UI
from ui import renderer, menu

init() # For colorama

def main():
    # Main Menu
    config = menu.show_main_menu()
    
    # Game Init
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    storage.init_history(start_fen)
    current_fen = start_fen
    
    # AI Setup
    ai_color = None
    if config['mode'] == 'pve':
        # If Player is White, AI is Black.
        ai_color = 'b' if config['color'] == 'w' else 'w'

    # UI State
    highlights = []
    error_pos = None
    last_move_coords = [] # Tracks [start_pos, end_pos]
    message = f"Mode: {config['mode'].upper()}"

    while True:
        board = create_board(current_fen)
        board_data = get_board_data(current_fen)
        turn = board_data["turn"]
        
        # Check Game Status
        game_status = arbiter.get_game_state(
            board, turn, board_data["en_passant"], board_data["castling_rights"]
        )

        # Check for King Check. We will use it to mark check position in renderer.
        check_pos = None
        if arbiter.is_king_in_check(board, turn):
            target = 'K' if turn == 'w' else 'k'
            for r in range(8):
                for c in range(8):
                    if board[r][c] == target:
                        check_pos = (r, c)
                        break

        # Render
        renderer.draw_game_state(
            board, turn, game_status, 
            highlights, error_pos, check_pos, last_move_coords, message
        )
        
        # Reset the highlights
        highlights = []
        error_pos = None
        message = ""

        if game_status != "PLAYING":
            renderer.get_player_input(turn)
            break

        # AI TURN
        if config['mode'] == 'pve' and turn == ai_color:
            print(f"  AI is thinking...")
            try:
                best_move = ai.get_best_move(current_fen)
                if best_move:
                    current_fen = update_board_state(best_move, current_fen)
                    storage.save_snapshot(current_fen)
                    
                    # Update Last Move Highlight
                    ai_start = change_notations(best_move[0:2])
                    ai_end = change_notations(best_move[2:4])
                    last_move_coords = [ai_start, ai_end]
                    continue
            except Exception as e:
                message = f"AI Error: {e}"

        # HUMAN TURN
        user_input = renderer.get_player_input(turn)

        # Helpful commands you can use.
        # 1. Quit
        if user_input.lower() in ['q', 'quit', 'exit']:
            break
        
        # 2. Undo
        if user_input.lower() in ['u', 'undo']:
            steps = 2 if config['mode'] == 'pve' else 1
            for _ in range(steps):
                prev = storage.undo_move()
                if prev: current_fen = prev
            message = "Undid move."
            last_move_coords = [] # Clear highlight on undo
            continue

        # 3. Help
        if user_input.startswith("?"):
            query = user_input[1:]
            # Help Position (?e2)
            if len(query) == 2 and query[1].isdigit():
                try:
                    pos = change_notations(query)
                    moves = arbiter.get_legal_moves(board, pos, board_data["en_passant"], board_data["castling_rights"])
                    highlights = moves
                    message = f"Found {len(moves)} legal moves."
                except: message = "Invalid coord."
            continue

        # 4. Move Execution
        if len(user_input) != 4:
            message = "Invalid format."
            continue

        try:
            start_pos = change_notations(user_input[0:2])
            end_pos = change_notations(user_input[2:4])
            
            if not (0 <= start_pos[0] < 8):
                message = "Out of bounds."
                continue

            legal_moves = arbiter.get_legal_moves(
                board, start_pos, board_data["en_passant"], board_data["castling_rights"]
            )

            if end_pos in legal_moves:
                current_fen = update_board_state(user_input, current_fen)
                storage.save_snapshot(current_fen)
                last_move_coords = [start_pos, end_pos]
            else:
                # Auto-Assist if the player makes an illegal move
                highlights = legal_moves
                error_pos = start_pos
                message = "Illegal move."
                
        except Exception as e:
            message = f"Error: {e}"

if __name__ == "__main__":
    main()
