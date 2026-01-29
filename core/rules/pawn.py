from core.rules import base
from core.utils import *

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int], en_passant_target: str = "-") -> list[tuple[int, int]]:
    """
    Calculates all pseudo-legal moves for a pawn at a specific position.
    Also includes en passant for cultured people.
    
    Args:
        board: The 2D board list.
        pos: Tuple (row, col) of the pawn.
        en_passant_target: The square (e.g., 'e3') that can be captured via en passant. 
    Returns:
        List of target tuples [(r, c), ...].
    """
    moves: list[tuple[int, int]] = []
    
    # Get Basic Info
    color = base.get_piece_color(board, pos)
    if color is None:
        return [] # Should not happen if logic is correct, but just in case.

    row, col = pos

    # White pawns go upwards (which mean row goes from 7 to 0, thus -1 is the direction). Black works the opposite.
    direction = -1 if color == "w" else 1
    start_row = 6 if color == "w" else 1

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

    # Capture Logic (Diagonals)
    # The two squares diagonally in front (or back)
    left_diag = (row + direction, col - 1)
    right_diag = (row + direction, col + 1)
    
    potential_captures = [left_diag, right_diag]

    for target in potential_captures:
        if base.is_on_board(target) and base.is_enemy(board, target, color):
            moves.append(target)

    # En Passant Logic
    if en_passant_target != "-":
        ep_coords = change_notations(en_passant_target)

        for target in potential_captures: # The kill check works exactly like normal pawn capture. The front two diagonal squares. 
            if base.is_on_board(target) and base.get_piece_on_position(board, target) == "+" and target == ep_coords: # Only works on empty squares. Well logically its impossible but whatever.
                moves.append(target)

    return moves
