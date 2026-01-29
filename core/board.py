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
    Executes a move and handles ALL the side effects (Castling, En Passant, Promotion, Rights Update).

    Args:
        move: a str in the format 'e2e4' (start_pos + end_pos)
        fen_string: the current fen string.
    Returns:
        str: The fully updated FEN string.
    """
    board = create_board(fen_string)
    board_data = get_board_data(fen_string)
    
    # Parse Coordinates
    start_str, end_str = move[0:2], move[2:4]
    start_pos = change_notations(start_str)
    end_pos = change_notations(end_str)
    
    piece = base.get_piece_on_position(board, start_pos)
    if piece is None or piece == "+": 
        return fen_string # Just in case
    
    p_type = piece.lower()
    color = "w" if piece.isupper() else "b"
    
    # Castling
    # We detect a castle if the King moves more than 1 column.
    if p_type == 'k' and abs(start_pos[1] - end_pos[1]) > 1: # Abs always gives the magnitude or just the positive value
        # King is at (7, 4) moving to (7, 6) [Kingside]
        if end_pos[1] > start_pos[1]: # Kingside
            rook_col, rook_dest_col = 7, 5 # h-file to f-file
        else: # Queenside
            rook_col, rook_dest_col = 0, 3 # a-file to d-file
            
        # Move the Rook
        row = start_pos[0]
        rook_piece = board[row][rook_col]
        board[row][rook_col] = "+"
        board[row][rook_dest_col] = rook_piece

    # En Passant
    # If a pawn moves diagonally into an empty square, it must be En Passant.
    if p_type == 'p':
        if start_pos[1] != end_pos[1] and board[end_pos[0]][end_pos[1]] == "+":
            # The victim is 'behind' the landing spot. What is this move, some anime? Omae wa mou shindeiru?!
            # White captures 'Up' (-1), so victim is 'Down' (+1).
            victim_dir = 1 if color == 'w' else -1
            board[end_pos[0] + victim_dir][end_pos[1]] = "+"

    # Moving the actual pawn
    board[start_pos[0]][start_pos[1]] = "+"
    board[end_pos[0]][end_pos[1]] = piece

    # Pawn promotion (This piece is really in his own anime)
    # If a pawn hits the last rank
    if p_type == 'p':
        if (color == 'w' and end_pos[0] == 0) or (color == 'b' and end_pos[0] == 7):
            # Auto-Promote to Queen for now
            board[end_pos[0]][end_pos[1]] = "Q" if color == 'w' else "q"


    # Fen metadata updates
    current_rights = str(board_data["castling_rights"])
    new_en_passant = "-"
    
    # Updating Castling Rights
    # If King moves, lose all rights for that color
    if p_type == 'k':
        if color == 'w':
            current_rights = current_rights.replace("K", "").replace("Q", "")
        else:
            current_rights = current_rights.replace("k", "").replace("q", "")
            
    # If Rook moves, lose rights for that side
    # White Rooks: a1 (7,0), h1 (7,7). Black Rooks: a8 (0,0), h8 (0,7)
    elif p_type == 'r':
        if start_pos == (7, 0):
            current_rights = current_rights.replace("Q", "")
        if start_pos == (7, 7): 
            current_rights = current_rights.replace("K", "")
        if start_pos == (0, 0):
            current_rights = current_rights.replace("q", "")
        if start_pos == (0, 7): 
            current_rights = current_rights.replace("k", "")

    # If Rook DIES, lose rights for that side
    if end_pos == (0, 0):
        current_rights = current_rights.replace("q", "")
    if end_pos == (0, 7):
        current_rights = current_rights.replace("k", "")
    if end_pos == (7, 0):
        current_rights = current_rights.replace("Q", "")
    if end_pos == (7, 7):
        current_rights = current_rights.replace("K", "")
    
    if current_rights == "":
        current_rights = "-" # Thats just how fen strings work.


    # Setting En Passant Target
    # If a pawn moves 2 squares, the space in between is the target.
    if p_type == 'p' and abs(start_pos[0] - end_pos[0]) == 2:
        skipped_row = (start_pos[0] + end_pos[0]) // 2 # Is always either 3 or 6
        # Convert back to notation (e.g., e3)
        col_char = chr(start_pos[1] + 97) # chr is the opposite of ord()
        rank_num = 8 - skipped_row
        new_en_passant = f"{col_char}{rank_num}"


    # Updating Timers & Turn
    next_turn = "w" if board_data["turn"] == "b" else "b"
    
    # Half move clock resets on Pawn Move or Capture. Otherwise +1.
    is_capture = (base.get_piece_on_position(create_board(fen_string), end_pos) != "+") # Check old board for capture. The new board has already changed so we can't check there.
    if p_type == 'p' or is_capture:
        half_timer = 0
    else:
        half_timer = int(board_data["half_timer"]) + 1

    full_timer = int(board_data["full_timer"]) + 1 if next_turn == "w" else int(board_data["full_timer"])

    
    return change_board_to_fen(
        board, 
        turn=next_turn, 
        castling_rights=current_rights,
        en_passant=new_en_passant,
        half_timer=half_timer,
        full_timer=full_timer
    )
