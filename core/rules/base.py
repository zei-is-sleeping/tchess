
def is_on_board(pos):
    return 0 <= pos[0] < 8 and 0 <= pos[1] < 8


def get_piece_on_position(board, pos):
    return board[pos[0]][pos[1]] if is_on_board(pos) else None


def get_piece_color(board, pos):
    piece = board[pos[0]][pos[1]] if is_on_board(pos) else None
    if piece == None or piece == "+":
        return None 
    return "w" if piece.isupper() else "b"
    

def is_friendly(board, pos, color):
    if get_piece_color(board, pos) == color:
        return True 
    return False


def is_enemy(board, pos, color):
    ex_color = get_piece_color(board, pos)
    if ex_color != color and ex_color != None:
        return True 
    return False


