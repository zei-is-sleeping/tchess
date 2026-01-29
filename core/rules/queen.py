from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Calculates all pseudo-legal moves for a queen at a specific position.

    Logic:
        Directions: (Row change, Col change).
        (-1, 0) = Up, (1, 0) = Down and so on.
        It is basically a merge of bishop directions and rook directions.
    
    Args:
        board: The 2D board list.
        pos: Tuple (row, col) of the pawn.
        
    Returns:
        List of target tuples [(r, c), ...].
    """
    straight = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal =   [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return base.get_sliding_moves(board, pos, straight + diagonal)
