from core.rules import base

def get_pseudo_legal_moves(board: list[list[str]], pos: tuple[int, int], castling_rights: str = "-") -> list[tuple[int, int]]:
    """
    Calculates pseudo-legal moves for a King, including Castling.
    
    Args:
        board: The board list.
        pos: King's position.
        castling_rights: 'KQkq' string from FEN.
    Returns:
        list[tuple[int, int]]: The list of valid moves.
    """
    moves: list[tuple[int, int]] = []
    color = str(base.get_piece_color(board, pos)) 
    row, col = pos
    
    # Normal King Moves
    possible_positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for pr, pc in possible_positions:
        test_pos = (row + pr, col + pc)
        if not base.is_on_board(test_pos): 
            continue
        if base.is_friendly(board, test_pos, color): 
            continue
        moves.append(test_pos)
        
    # Castling Logic
    # Hardcoded Ranks/Cols for standard chess. We won't be managing rooks here.
    # White King is at (7, 4) [e1]. Kingside -> (7, 6) [g1]. Queenside -> (7, 2) [c1].
    # Black King is at (0, 4) [e8]. Kingside -> (0, 6) [g8]. Queenside -> (0, 2) [c8].
    
    if color == 'w':
        # Kingside (K)
        if 'K' in castling_rights:
            # Check if f1(7,5) and g1(7,6) are empty
            if base.get_piece_on_position(board, (7, 5)) == "+" and base.get_piece_on_position(board, (7, 6)) == "+":
                moves.append((7, 6)) # Move 2 squares right
        
        # Queenside (Q)
        if 'Q' in castling_rights:
            # Check if d1(7,3), c1(7,2), b1(7,1) are empty
            if base.get_piece_on_position(board, (7, 3)) == "+" and base.get_piece_on_position(board, (7, 2)) == "+" and base.get_piece_on_position(board, (7, 1)) == "+":
                moves.append((7, 2)) # Move 2 squares left

    else: # Black
        # Kingside (k)
        if 'k' in castling_rights:
             if base.get_piece_on_position(board, (0, 5)) == "+" and base.get_piece_on_position(board, (0, 6)) == "+":
                moves.append((0, 6))

        # Queenside (q)
        if 'q' in castling_rights:
            if base.get_piece_on_position(board, (0, 3)) == "+" and base.get_piece_on_position(board, (0, 2)) == "+" and base.get_piece_on_position(board, (0, 1)) == "+":
                moves.append((0, 2))

    return moves
