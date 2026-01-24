def change_fen_to_row(data):
    row = ""
    for char in data:
        if char.isdigit():
            row += "+" * int(char)
        else:
            row += char
    return row


def create_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    placement_data = fen_string.split()[0].strip().split("/")
    board = []
    for data in placement_data:
        row = change_fen_to_row(data)
        board.append(row)
    return board


def change_notations(position):
    return (8 - int(position[1]), ord(position[0]) - 97)


def get_piece_on_position(position, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    board = create_board(fen_string)
    return board[position[0]][position[1]]


def change_board_to_fen(board, active_color = "w", casting_rights = "KQkq", en_passant = "-", halfmove_clock = 0, fullmove_number = 1):
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
    fen_string += f" {active_color} {casting_rights} {en_passant} {halfmove_clock} {fullmove_number}"

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

    # TODO: other parts of fen_string
    

