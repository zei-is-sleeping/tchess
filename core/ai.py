import subprocess
import os
import sys
import time

class Stockfish:
    def __init__(self, difficulty_level=1):
        """
        Difficulty: 
        1 = Monkey (Skill 0, Depth 1)
        2 = Beginner (Skill 5, Depth 5)
        3 = Average (Skill 10, 1 sec)
        4 = God (Skill 20, 2 sec)
        """
        self.process = None
        self.difficulty = difficulty_level
        self.path = self._get_binary_path()

    def _get_binary_path(self):
        base_path = os.getcwd()
        if os.name == 'nt': # Windows
            return os.path.join(base_path, "bin", "stockfish_win.exe")
        else: # Linux
            return os.path.join(base_path, "bin", "stockfish_linux")

    def _start_engine(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Engine not found at {self.path}. Did you create the 'bin' folder?")
            
        # Start the process with pipes
        self.process = subprocess.Popen(
            self.path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self._send_command("uci")
        self._wait_for_ready()

    def _send_command(self, cmd):
        if self.process and self.process.poll() is None:
            self.process.stdin.write(f"{cmd}\n")
            self.process.stdin.flush()

    def _wait_for_ready(self):
        while True:
            line = self.process.stdout.readline().strip()
            if line == "uciok" or line == "readyok":
                break

    def get_best_move(self, fen):
        """
        Sends the FEN to Stockfish and waits for the move.
        """
        # Restart engine for each move to ensure clean state (easiest for school projects)
        # In a real app, you'd keep it running, but this avoids sync bugs.
        self._start_engine()
        
        # Configure Difficulty
        skill_map = {1: 0, 2: 5, 3: 10, 4: 20}
        movetime_map = {1: 100, 2: 500, 3: 1000, 4: 2000}
        depth_map = {1: 1, 2: 5, 3: 10, 4: 15}

        self._send_command(f"setoption name Skill Level value {skill_map.get(self.difficulty, 10)}")
        self._send_command("isready")
        self._wait_for_ready()

        # Send Board
        self._send_command(f"position fen {fen}")
        
        # Ask for Move
        if self.difficulty <= 2:
            self._send_command(f"go depth {depth_map[self.difficulty]}")
        else:
            self._send_command(f"go movetime {movetime_map[self.difficulty]}")

        # Read Output
        best_move = None
        while True:
            line = self.process.stdout.readline().strip()
            if line.startswith("bestmove"):
                # Format: "bestmove e2e4 ponder ..."
                best_move = line.split()[1]
                break
        
        # Kill process to save RAM
        self.process.terminate()
        return best_move
