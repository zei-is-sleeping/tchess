import subprocess
import os

def get_binary_path() -> str:
    """
    Locates the Stockfish binary in the 'bin' folder.
    It automatically detects if we are on Windows or Linux because
    I use linux and I want linux support.
    """
    base_path = os.getcwd()
    if os.name == 'nt': # Windows
        return os.path.join(base_path, "bin", "stockfish_win.exe")
    else: # Linux
        return os.path.join(base_path, "bin", "stockfish_linux")


def send_command(process: subprocess.Popen, cmd: str):
    """
    Helper to write to the engine's stdin.
    """
    if process and process.poll() is None:
        process.stdin.write(f"{cmd}\n")
        process.stdin.flush()


def get_best_move(fen: str, difficulty: int = 1) -> str | None:
    """
    This function spins up a Stockfish process, feeds it the current board state (FEN),
    drugs it based on the difficulty level (by limiting its thinking time), 
    and extracts the best move it can find.
    
    Args:
        fen: The current board state string.
        difficulty: 1 (Monkey) to 4 (Grandmaster).
        
    Returns:
        A move string like 'e2e4', or None if the engine crashes/fails. I hope it doesn't.
    """
    path = get_binary_path()
    
    if not os.path.exists(path):
        # If the binary is missing, we can't really do anything.
        raise FileNotFoundError(f"Stockfish binary not found at {path}")

    # Start the Engine Process
    # We open pipes to stdin (to talk to it) and stdout (to listen to it).
    process = subprocess.Popen(
        path,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    try:
        # Configure the Engine
        # 'uci' tells the engine to wake up.
        send_command(process, "uci")
        
        # Difficulty Configuration
        # We limit the engine using 'Skill Level' (0-20) and 'movetime' (ms)
        # Level 1: Skill 0, Depth 1 (Basically random valid moves)
        # Level 2: Skill 5, Depth 5
        # Level 3: Skill 10, 1000ms
        # Level 4: Skill 20, 2000ms
        
        skill_map = {1: 0, 2: 5, 3: 10, 4: 20}
        movetime_map = {1: 100, 2: 500, 3: 1000, 4: 2000}
        depth_map = {1: 1, 2: 5, 3: 10, 4: 15}
        
        skill = skill_map.get(difficulty, 10)
        send_command(process, f"setoption name Skill Level value {skill}")
        send_command(process, "isready")
        
        # Wait for the engine to finish loading (it usually replies 'readyok')
        while True:
            line = process.stdout.readline().strip()
            if line == "readyok": break

        # Send the Board
        send_command(process, f"position fen {fen}")
        
        # Ask for the Move
        if difficulty <= 2:
            # For low levels, limit depth so it plays bad on purpose
            send_command(process, f"go depth {depth_map[difficulty]}")
        else:
            # For high levels, give it time to think
            send_command(process, f"go movetime {movetime_map[difficulty]}")

        # Read the Result
        best_move = None
        while True:
            line = process.stdout.readline().strip()
            # The engine eventually prints 'bestmove e2e4 ponder ...'
            if line.startswith("bestmove"):
                best_move = line.split()[1]
                break
                
        return best_move

    except Exception as e:
        # Something went wrong. Hopefully it won't.
        print(f"Engine Error: {e}")
        return None
        
    finally:
        # Cleanup
        # We don't want orphan chess engines eating RAM.
        process.terminate()

