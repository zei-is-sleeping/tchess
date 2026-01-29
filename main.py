import sys
import colorama
from core import create_board, update_board_state
from ui import print_board_high_res

colorama.init()
board = create_board()
print_board_high_res(board)
