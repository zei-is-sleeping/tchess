import pickle

HISTORY_FILE = "data/history.dat"

def init_history(initial_fen: str):
    """
    Resets the history file and saves the starting position.
    """
    # Overwrite file with initial state list
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump([initial_fen], f)

def save_snapshot(fen: str):
    """
    Appends the new FEN state to the history.
    """
    try:
        with open(HISTORY_FILE, "rb") as f:
            history = pickle.load(f)
    except (FileNotFoundError, EOFError):
        history = []

    history.append(fen)

    # Write back
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(history, f)

def undo_move() -> str | None:
    """
    Removes the latest state and returns the previous FEN.
    Returns None if undo is not possible (at start).
    """
    try:
        with open(HISTORY_FILE, "rb") as f:
            history = pickle.load(f)
    except (FileNotFoundError, EOFError):
        return None

    if len(history) <= 1:
        return None # Cannot undo start state

    # Remove the last move
    history.pop()

    # Save new history
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(history, f)

    # Return the new 'current' state (the one at the end of the list)
    return history[-1]
