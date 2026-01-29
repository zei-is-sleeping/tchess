from core.utils import change_fen_to_row, change_notations

def create_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    placement_data = fen_string.split()[0].strip().split("/")
    board = []
    for data in placement_data:
        row = change_fen_to_row(data)
        board.append(row)
    return board


def get_board_data(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    placement_data = fen_string.split()[1:]
    data = {
        "turn": placement_data[0],
        "castling_rights": placement_data[1],
        "en_passant": placement_data[2],
        "half_timer": int(placement_data[3]),
        "full_timer": int(placement_data[4])
        }
    return data


def change_board_to_fen(board, turn = "w", castling_rights = "KQkq", en_passant = "-", half_timer = 0, full_timer = 1):
    fen_string = ""
    for row in board:
        spaces = 0
        for char in row:
            if char == "+":
                spaces += 1
            elif char != "+" and spaces > 0:
                fen_string += str(spaces) + char                
                spaces = 0
            else:
                fen_string += char 
        if spaces > 0:
            fen_string += str(spaces)
        fen_string += r"/"
    
    fen_string = fen_string[:-1]
    fen_string += f" {turn} {castling_rights} {en_passant} {half_timer} {full_timer}"

    return fen_string


def update_board_state(move, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    board = create_board(fen_string)

    current_position = change_notations(move[0:2])
    piece = get_piece_on_position(current_position)
    new_position = change_notations(move[2:4])

    old_row = board[current_position[0]]
    updated_old_row = old_row[0:current_position[1]] + "+" + old_row[current_position[1] + 1:]
    board[current_position[0]] = updated_old_row

    new_row = board[new_position[0]]
    updated_new_row = new_row[0:new_position[1]] + piece + new_row[new_position[1] + 1:]
    board[new_position[0]] = updated_new_row

    board_data = get_board_data(fen_string)
    turn = "w" if board_data["turn"] == "b" else "b"
    full_timer = board_data["full_timer"] + 1
    # TODO: other parts of fen_string like en_passant, castling rights, etc.

    updated_fen_string = change_board_to_fen(board, turn = turn, full_timer = full_timer)
    return updated_fen_string

