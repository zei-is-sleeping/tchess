def change_fen_to_row(data):
    row = ""
    for char in data:
        if char.isdigit():
            row += "+" * int(char)
        else:
            row += char
    return row


def change_notations(position):
    return (8 - int(position[1]), ord(position[0]) - 97)


