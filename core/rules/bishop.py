from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Calculates all pseudo-legal moves for a bishop at a specific position.

    Logic:
        Directions: (Row change, Col change).
        (1, 1) = Bottom Right, (-1, 1) = Top Right and so on.
    
    Args:
        board: The 2D board list.
        pos: Tuple (row, col) of the pawn.
        
    Returns:
        List of target tuples [(r, c), ...].
    """
    diagonal_directions = [(-1, -1), (-1,  1), ( 1, -1), ( 1,  1)]
    return base.get_sliding_moves(board, pos, diagonal_directions)
