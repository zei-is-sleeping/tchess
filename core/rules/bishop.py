from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Bishop Movement: Diagonal Sliding.
    """
    # Directions: (Row Change, Col Change)
    diagonal_directions = [
        (-1, -1), # Top-Left
        (-1,  1), # Top-Right
        ( 1, -1), # Bottom-Left
        ( 1,  1)  # Bottom-Right
    ]
    
    return base.get_sliding_moves(board, pos, diagonal_directions)
