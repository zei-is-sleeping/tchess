def is_on_board(pos: tuple[int, int]) -> bool:
    """
    Checks if the coordinates are within the 8x8 grid.
    """
    return 0 <= pos[0] < 8 and 0 <= pos[1] < 8


def get_piece_on_position(board: list[list[str]], pos: tuple[int, int]) -> str | None:
    """
    Returns the character at the given position, or None if out of bounds.
    """
    if is_on_board(pos):
        return board[pos[0]][pos[1]]
    return None


def get_piece_color(board: list[list[str]], pos: tuple[int, int]) -> str | None:
    """
    Returns 'w' for White, 'b' for Black, or None if empty/invalid.
    """
    piece = get_piece_on_position(board, pos)
    
    if piece is None or piece == "+":
        return None 
    
    return "w" if piece.isupper() else "b"
    

def is_friendly(board: list[list[str]], pos: tuple[int, int], color: str) -> bool:
    """
    Returns True if the piece at pos belongs to the given color.
    """
    if get_piece_color(board, pos) == color:
        return True 
    return False


def is_enemy(board: list[list[str]], pos: tuple[int, int], color: str) -> bool:
    """
    Returns True if the piece at pos belongs to the OPPOSITE color.
    """
    ex_color = get_piece_color(board, pos)
    if ex_color is not None and ex_color != color:
        return True 
    return False


def get_sliding_moves(board: list[list[str]], pos: tuple[int, int], directions: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Generic raycasting generator for sliding pieces (Rook, Bishop, Queen).
    Args:
        board: board list
        pos: starting position (row, col)
        directions: List of (row_change, col_change) tuples. 
                    e.g. [(1, 0)] means 'Down'.
    """
    moves: list[tuple[int, int]] = []
    color = str(get_piece_color(board, pos))
    
    for dr, dc in directions:
        row, col = pos
        
        # Keep walking in this direction
        while True:
            row += dr
            col += dc
            target = (row, col)
            
            # 1. Check if the ray is leaking out
            if not is_on_board(target):
                break
            
            # 2. Check Obstacles
            if is_friendly(board, target, color):
                break # Blocked by friendly piece
            
            # 3. Valid Move
            moves.append(target)
            
            if is_enemy(board, target, color):
                break # Capture enemy, then stop (can't jump over)
                
    return moves
