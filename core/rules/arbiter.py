from core.rules import base, pawn, rook, knight, bishop, queen, king

def get_pseudo_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Collects all possible pseudo-legal moves on the board for one piece.
    "Pseudo-legal" means it follows geometry (L-shapes, diagonals) but ignores 
    King safety.

    Args:
        board: The 2D board list.
        pos: The (row, col) tuple of the piece.
    Returns: 
        A list of position coordinates [(r, c), ...].
    """
    piece_char = base.get_piece_on_position(board, pos)
    if not piece_char or piece_char == "+":
        return []
        
    p_type = piece_char.lower()
    
    if p_type == 'p': return pawn.get_pseudo_legal_moves(board, pos)
    if p_type == 'r': return rook.get_pseudo_legal_moves(board, pos)
    if p_type == 'n': return knight.get_pseudo_legal_moves(board, pos)
    if p_type == 'b': return bishop.get_pseudo_legal_moves(board, pos)
    if p_type == 'q': return queen.get_pseudo_legal_moves(board, pos)
    if p_type == 'k': return king.get_pseudo_legal_moves(board, pos)
    
    return []


def is_square_under_attack(board: list[list[str]], pos: tuple[int, int], defender_color: str) -> bool:
    """
    Checks if a specific square is under attack by the enemy.
    
    Logic:
    Instead of checking every enemy piece, we sit at 'pos' and pretend to be different pieces.
    - If we pretend to be a Knight and land on an enemy Knight, we are under attack by a Knight.
    - If we pretend to be a Rook and see an enemy Rook, we are under attack by a Rook.
    
    Args:
        board: The 2D board list.
        pos: The target (row, col) to check safety for.
        defender_color: The color of the side we are checking safety for ('w' or 'b').
                        (We look for attackers of the OPPOSITE color).
                        
    Returns:
        True if the square is being attacked, False otherwise.
    """
    
    # Check for Knights
    for test_pos in knight.get_pseudo_legal_moves(board, pos):
        p = base.get_piece_on_position(board, test_pos)
        if p and p.lower() == 'n' and base.is_enemy(board, test_pos, defender_color): 
            return True

    # Queens don't get their own check because they are just rooks and bishops in a trench coat
    # Check for Rooks/Queens
    for test_pos in rook.get_pseudo_legal_moves(board, pos):
        p = base.get_piece_on_position(board, test_pos)
        if p and p.lower() in ['r', 'q'] and base.is_enemy(board, test_pos, defender_color):
            return True

    # Check for Bishops/Queens
    for test_pos in bishop.get_pseudo_legal_moves(board, pos):
        p = base.get_piece_on_position(board, test_pos)
        if p and p.lower() in ['b', 'q'] and base.is_enemy(board, test_pos, defender_color):
            return True

    # Check for Pawns
    row, col = pos
    # If Defender is White, Enemy is Above (Row - 1). 
    # If Defender is Black, Enemy is Below (Row + 1).
    pawn_direction = -1 if defender_color == 'w' else 1 

    attack_positions = [
        (row + pawn_direction, col - 1),
        (row + pawn_direction, col + 1)
    ]
    
    for attack_pos in attack_positions:
        if base.is_on_board(attack_pos):
            p = base.get_piece_on_position(board, attack_pos)
            if p and p.lower() == 'p' and base.is_enemy(board, attack_pos, defender_color):
                return True
                
    # Check for King
    for test_pos in king.get_pseudo_legal_moves(board, pos):
        p = base.get_piece_on_position(board, test_pos)
        if p and p.lower() == 'k' and base.is_enemy(board, test_pos, defender_color):
            return True

    return False


def is_king_in_check(board: list[list[str]], color: str) -> bool:
    """
    Wrapper function that finds the King and checks if his square is under attack.

    Args:
        board: The 2D board list.
        color: The color of the King ('w' or 'b').

    Returns:
        True if the King is in check, False otherwise.
    """
    king_pos = None
    target_char = 'K' if color == 'w' else 'k'
    
    # Find the King's coordinates
    for r in range(8):
        for c in range(8):
            if board[r][c] == target_char:
                king_pos = (r, c)
                break
        if king_pos: break # Prevents looping needlessly once the king is found
        
    # If King is not found somehow, lets just say the game is over 
    if not king_pos:
        return True 

    # Check if that square is under attack
    return is_square_under_attack(board, king_pos, color)


def get_legal_moves(board: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns the FINAL list of moves a piece can make.
    
    Process:
    1. Get all pseudo-legal moves (geometry only).
    2. Simulate each move on a temporary board.
    3. Check if the move leaves the King in check.
    4. If King is safe, the move is Legal.
    5. Cry that this logic might be too heavy.

    Args:
        board: The 2D board list.
        pos: The starting position (row, col).

    Returns:
        List of valid target tuples, [(row, col), ...].
    """
    # Get raw geometry moves
    pseudo_moves = get_pseudo_moves(board, pos)
    legal_moves: list[tuple[int, int]] = []
    
    color = base.get_piece_color(board, pos)
    if not color: return [] # If there's no color, there's no piece and thus no possible moves
    
    # Simulate each move
    for target in pseudo_moves:
        # We need a deep copy so our board isn't destroyed. Lists are weird in python. I am not going to use the copy library though. 
        temp_board = [row[:] for row in board]
        
        # Simulating the move
        piece = temp_board[pos[0]][pos[1]]
        temp_board[target[0]][target[1]] = piece
        temp_board[pos[0]][pos[1]] = "+"
        
        # Check Safety
        if not is_king_in_check(temp_board, color):
            legal_moves.append(target)
            
    return legal_moves
