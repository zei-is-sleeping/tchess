from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Rook Movement: Straight Sliding (Up, Down, Left, Right).
    # Directions: (Row Change, Col Change)
    # (-1, 0) = Up
    # ( 1, 0) = Down
    # ( 0,-1) = Left
    # ( 0, 1) = Right
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    return base.get_sliding_moves(board, pos, directions)
