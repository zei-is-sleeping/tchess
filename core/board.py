from core.utils import change_fen_to_row, change_notations
from core.rules import base 

def create_board(fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> list[list[str]]:
    """
    Parses a FEN string and returns a 2D list representing the board.

    Logic:
        The board becomes a nested list which contains positions and pieces. 
        + means the position is empty.
        Uppercase letters mean the position is occupied by a white piece.
        Lowercase letters mean the position is occupied by a black piece. 

    Args:
        fen_string: A complete fen string. If you don't provide one, it starts with a default fen_string.
    Returns:
        The board list.
    """
    placement_data = fen_string.split()[0].strip().split("/")
    board: list[list[str]] = []
    for data in placement_data:
        row = change_fen_to_row(data)
        board.append(list(row)) # Explicitly convert string to list for mutability
    return board


def get_board_data(fen_string: str) -> dict[str, str | int]:
    """
    Extracts metadata (turn, castling rights, etc.) from a FEN string.

    Args:
        fen_string: must provide your own fen_string of the board.
    Result: 
         A dictionary containing different keys corresponding to the different parts of a fen string.
    """
    placement_data = fen_string.split()[1:]
    
    data = {
        "turn": placement_data[0],
        "castling_rights": placement_data[1],
        "en_passant": placement_data[2],
        "half_timer": int(placement_data[3]),
        "full_timer": int(placement_data[4])
    }
    return data


def change_board_to_fen(board: list[list[str]], turn: str = "w", castling_rights: str = "KQkq", en_passant: str = "-", half_timer: int = 0, full_timer: int = 1) -> str:
    """
    Compresses the current board state into a FEN string.

    Logic:
        A fen string is made up of 5 components.
        Board state: Here, each row of the board is described in a string which is then separated with a /. For example, 3pr3. Numbers mean n number of empty spaces. The characters tell the piece and the color of the piece. Capital means white. 
        Turn: Tells which color is to move currently.
        Castling Rights: Tells if the king of both colors can castle, and if yes, in which sides? k means king's side. q means queen's side. - means no king can castle at all. Capital means white.
        En Passant check: Stores the board coordinate if a pawn skipped that coordinate in a double jump on its first move last turn. Now if a pawn does en passant, it will end up on this coordinate.
        Half timer: How many turns has it been since a pawn development or a piece capture? Usually if this reaches 50, its a draw.
        Full timer: How many total turns have passed?

    Args:
        board: The 2d board list 
        turn, castling_rights, en_passant, half_timer, full_timer: as described above in logic.
    Returns:
        str: a fen string.
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
        
        # Handle remaining spaces in a row
        if spaces > 0:
            fen_string += str(spaces)
        fen_string += r"/"
    
    # stripping the last slash and appending metadata
    fen_string = fen_string[:-1]
    fen_string += f" {turn} {castling_rights} {en_passant} {half_timer} {full_timer}"

    return fen_string


def update_board_state(move: str, fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> str:
    """
    Executes a move (DOES NOT INCLUDE LEGITIMACY) and returns an updated fen string.

    Args:
        move: a str in the format 'e2e4' (start_pos + end_pos)
        fen_string: the current fen string, from which the next fen string will be generated. 
    Returns:
        str: Updated fen string with the move successfully done. Automatically handles taking pieces.
    """
    board = create_board(fen_string)

    # Parse coordinates
    current_position = change_notations(move[0:2])
    new_position = change_notations(move[2:4])
    
    piece = base.get_piece_on_position(board, current_position)
    # Just in case.
    if piece is None:
        return fen_string

    # Empty the original position
    board[current_position[0]][current_position[1]] = "+"

    # Place piece in new position
    board[new_position[0]][new_position[1]] = piece

    # Update Metadata
    board_data = get_board_data(fen_string)
    turn = "w" if board_data["turn"] == "b" else "b"
    full_timer = int(board_data["full_timer"]) + 1

    # TODO: Update en_passant targets and castling rights logic here later
    
    updated_fen_string = change_board_to_fen(board, turn=turn, full_timer=full_timer)
    return updated_fen_string
