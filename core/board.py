from core.utils import change_fen_to_row, change_notations
from core.rules import base 

def create_board(fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> list[list[str]]:
    """
    Parses a FEN string and returns a 2D list representing the board.
    Rank 8 is at index 0.
    """
    placement_data = fen_string.split()[0].strip().split("/")
    board: list[list[str]] = []
    for data in placement_data:
        row = change_fen_to_row(data)
        board.append(list(row)) # Explicitly convert string to list for mutability
    return board


def get_board_data(fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> dict[str, str | int]:
    """
    Extracts metadata (turn, castling rights, etc.) from a FEN string.
    """
    placement_data = fen_string.split()[1:]
    
    # Safety check for incomplete FENs
    if not placement_data:
        return {
            "turn": "w", 
            "castling_rights": "KQkq", 
            "en_passant": "-", 
            "half_timer": 0, 
            "full_timer": 1
        }

    data = {
        "turn": placement_data[0],
        "castling_rights": placement_data[1],
        "en_passant": placement_data[2],
        "half_timer": int(placement_data[3]),
        "full_timer": int(placement_data[4])
    }
    return data


def change_board_to_fen(board: list[list[str]], turn: str = "w", castling_rights: str = "KQkq", 
                       en_passant: str = "-", half_timer: int = 0, full_timer: int = 1) -> str:
    """
    Compresses the current board state into a FEN string.
    """
    fen_string = ""
    for row in board:
        spaces = 0
        for char in row:
            if char == "+":
                spaces += 1
            else:
                if spaces > 0:
                    fen_string += str(spaces)
                    spaces = 0
                fen_string += char 
        
        # Handle trailing spaces in a row
        if spaces > 0:
            fen_string += str(spaces)
        fen_string += r"/"
    
    # Remove the trailing slash and append metadata
    fen_string = fen_string[:-1]
    fen_string += f" {turn} {castling_rights} {en_passant} {half_timer} {full_timer}"

    return fen_string


def update_board_state(move: str, fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> str:
    """
    Executes a move in 'god mode' (no validation) and returns the new FEN string.
    Move format: 'e2e4' (start_pos + end_pos)
    """
    board = create_board(fen_string)

    # Parse coordinates
    current_position = change_notations(move[0:2])
    new_position = change_notations(move[2:4])
    
    # Retrieve piece using base module logic
    piece = base.get_piece_on_position(board, current_position)
    if piece is None:
        return fen_string

    # 1. Clear the old position (Mitosis fix)
    # We treat rows as lists now for easier mutation
    board[current_position[0]][current_position[1]] = "+"

    # 2. Place piece in new position
    board[new_position[0]][new_position[1]] = piece

    # 3. Update Metadata
    board_data = get_board_data(fen_string)
    turn = "w" if board_data["turn"] == "b" else "b"
    full_timer = int(board_data["full_timer"]) + 1

    # TODO: Update en_passant targets and castling rights logic here later
    
    updated_fen_string = change_board_to_fen(board, turn=turn, full_timer=full_timer)
    return updated_fen_string
