from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Calculates all pseudo-legal moves for a knight at a specific position.
    
    Args:
        board: The 2D board list.
        pos: Tuple (row, col) of the pawn.
        
    Returns:
        List of target tuples [(r, c), ...].
    """
    moves: list[tuple[int, int]] = []
    color = str(base.get_piece_color(board, pos)) 
    row, col = pos
    possible_positions = [(1, 2), (2, 1), (-1, 2), (1, -2), (-1, -2), (-2, -1), (-2, 1), (2, -1)]

    for pr, pc in possible_positions:
        test_pos = (row + pr, col + pc)

        # Check if the test position is even on board
        if not base.is_on_board(test_pos):
            continue

        # Check if a friendly piece is hogging space on the test position 
        if base.is_friendly(board, test_pos, color):
            continue

        # If neither of the two, the move is legal
        moves.append(test_pos)
        
    return moves
    
