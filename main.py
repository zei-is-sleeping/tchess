from colorama import init

# Import Core
from core.board import create_board, update_board_state, get_board_data
from core.rules import arbiter
from core.utils import change_notations
from core import storage

# Import UI
from ui import renderer

init()

def main():
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    storage.init_history(start_fen)
    current_fen = start_fen
    
    # UI State
    highlights = []  # Green squares
    error_pos = None # Red square (illegal source)
    message = ""     # Info text

    while True:
        board = create_board(current_fen)
        board_data = get_board_data(current_fen)
        turn = board_data["turn"]
        
        # Check Game State
        game_status = arbiter.get_game_state(
            board, turn, board_data["en_passant"], board_data["castling_rights"]
        )

        # Detect Check for UI Highlighting
        check_pos = None
        if arbiter.is_king_in_check(board, turn):
            # Find King to paint him Red
            target = 'K' if turn == 'w' else 'k'
            for r in range(8):
                for c in range(8):
                    if board[r][c] == target:
                        check_pos = (r, c)
                        break

        # Render
        renderer.draw_game_state(
            board, turn, game_status, 
            highlights, error_pos, check_pos, message
        )
        
        # Reset transient UI state
        highlights = []
        error_pos = None
        message = ""

        # Input
        if game_status != "PLAYING":
            renderer.get_player_input(turn) # Just to pause
            break

        user_input = renderer.get_player_input(turn)

        # --- LOGIC ---

        # 1. Quit
        if user_input.lower() in ['q', 'quit', 'exit']:
            break
        
        # 2. Undo
        if user_input.lower() in ['u', 'undo']:
            prev_fen = storage.undo_move()
            if prev_fen:
                current_fen = prev_fen
                message = "Undid last move."
            else:
                message = "Cannot undo further."
            continue

        # 3. Help Command (?e2 or ?K)
        if user_input.startswith("?"):
            query = user_input[1:]
            
            # Case A: Position (?e2)
            if len(query) == 2 and query[1].isdigit():
                try:
                    pos = change_notations(query)
                    legal_moves = arbiter.get_legal_moves(
                        board, pos, board_data["en_passant"], board_data["castling_rights"]
                    )
                    highlights = legal_moves
                    if not legal_moves:
                        error_pos = pos # Highlight piece red if stuck
                        message = "No legal moves for this piece."
                    else:
                        message = f"Showing {len(legal_moves)} moves for {query}."
                except:
                    message = "Invalid coordinate."
                continue
            
            # Case B: Piece Type (?N, ?K) (Bonus)
            elif len(query) == 1:
                # Find all pieces of this type and color
                found = False
                for r in range(8):
                    for c in range(8):
                        p = board[r][c]
                        if p.upper() == query.upper() and \
                           (('w' in turn and p.isupper()) or ('b' in turn and p.islower())):
                            
                            moves = arbiter.get_legal_moves(board, (r, c), board_data["en_passant"], board_data["castling_rights"])
                            highlights.extend(moves)
                            found = True
                if not found:
                    message = f"No active {query} found."
                continue

        # 4. Move Execution
        if len(user_input) != 4:
            message = "Invalid format. Use 'e2e4' or '?e2'."
            continue

        try:
            start_pos = change_notations(user_input[0:2])
            end_pos = change_notations(user_input[2:4])
            
            # Bounds
            if not (0 <= start_pos[0] < 8 and 0 <= start_pos[1] < 8):
                message = "Out of bounds."
                continue

            # Get Legal Moves for Source
            legal_moves = arbiter.get_legal_moves(
                board, start_pos, board_data["en_passant"], board_data["castling_rights"]
            )

            if end_pos in legal_moves:
                current_fen = update_board_state(user_input, current_fen)
                storage.save_snapshot(current_fen)
            else:
                # AUTO-ASSIST: Highlight valid moves on error
                highlights = legal_moves
                error_pos = start_pos
                message = "Illegal move! Valid moves highlighted."
                
        except Exception as e:
            message = f"Error: {e}"

if __name__ == "__main__":
    main()
