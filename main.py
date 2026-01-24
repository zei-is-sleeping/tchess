def change_fen_to_row(data):
    row = ""
    for char in data:
        if char.isdigit():
            row += "+ " * int(char)
        else:
            row += char + " "
    return row


def print_board(fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    placement_data = fen_string.split()[0].strip().split("/")
    for y in range(1, 9):
        row = change_fen_to_row(placement_data[y - 1])
        print(row)

print_board()
print_board("r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
print_board("r3k2r/pppppppp/8/8/4P3/8/PPPP1PPP/R3K2R b KQkq e3 0 1")
