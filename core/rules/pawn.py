from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Calculates all pseudo-legal moves for a pawn at a specific position.
    
    Includes:
    - Single step forward (if empty)
    - Double step forward (if at start and path empty)
    - Diagonal captures (if enemy present)
    
    Does NOT include:
    - En Passant (requires FEN metadata)
    - Pin/Check checks (handled by Arbiter)
    
    Args:
        board: The 2D board list.
        pos: Tuple (row, col) of the pawn.
        
    Returns:
        List of target tuples [(r, c), ...].
    """
    moves: list[tuple[int, int]] = []
    
    # 1. Get Basic Info
    color = base.get_piece_color(board, pos)
    if color is None:
        return [] # Should not happen if logic is correct, but just in case.

    row, col = pos

    # 2. Determine Direction & Start Row
    # White (Index 6 -> 0) moves -1. Black (Index 1 -> 7) moves +1.
    direction = -1 if color == "w" else 1
    start_row = 6 if color == "w" else 1

    # 3. Forward Movement Logic
    # Check 1 Step Ahead
    forward_one = (row + direction, col) # Direction is automatically handled by the variable setting above.
    
    if base.is_on_board(forward_one) and base.get_piece_on_position(board, forward_one) == "+":
        moves.append(forward_one)

        # Check 2 Steps Ahead 
        # (Only allowed if 1st step was valid AND we are at start rank)
        if row == start_row:
            forward_two = (row + (direction * 2), col)
            if base.is_on_board(forward_two) and base.get_piece_on_position(board, forward_two) == "+":
                moves.append(forward_two)

    # 4. Capture Logic (Diagonals)
    # The two squares diagonally in front
    left_diag = (row + direction, col - 1)
    right_diag = (row + direction, col + 1)
    
    potential_captures = [left_diag, right_diag]

    for target in potential_captures:
        # Must be on board AND contain an ENEMY piece
        if base.is_on_board(target) and base.is_enemy(board, target, color):
            moves.append(target)

    return moves
