from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Queen Movement: All 8 Directions.
    """
    orthogonal = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal =   [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # The Queen is just a Rook and a Bishop taped together
    return base.get_sliding_moves(board, pos, orthogonal + diagonal)
