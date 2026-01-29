def change_fen_to_row(data: str) -> str:
    """
    Expands a FEN row string into a full board row string.
    Example: '3p4' -> '+++p++++'

    Args:
        data: Basically the string that exists between two slashes in a fen string.
    Returns:
        str: And expanded string where space numbers are replaced with accurate amounts of + symbols.
    """
    row = ""
    for char in data:
        if char.isdigit():
            row += "+" * int(char)
        else:
            row += char
    return row


def change_notations(position: str) -> tuple[int, int]:
    """
    Converts standard chess notation to matrix coordinates.
    Example: 'e4' -> (4, 4) [Rank 8 is index 0]
    
    Args:
        position (str): A string like 'e4' or 'a1'.
    Returns:
        tuple[int, int]: (row_index, col_index).
    """
    return (8 - int(position[1]), ord(position[0]) - 97)
