import tabulate
from main import BLACK, WHITE, EMPTY

class State(object):
    def __init__(self):
        self._board = [[EMPTY]*8 for _ in range(8)]
        self._board[3][3] = BLACK
        self._board[3][4] = WHITE
        self._board[4][3] = WHITE
        self._board[4][4] = BLACK

        self._current_player = BLACK

    def print_board(self, valid_moves = None):
        header = [str(col) for col in range(8)]
        if valid_moves:
            table = [[str(i)] + [self.cell_to_str(self._board[i][j]) if (i, j) not in valid_moves else '?' for j in range(8)] for i in range(8)]
        else:
            table = [[str(i)] + [self.cell_to_str(self._board[i][j]) for j in range(8)] for i in range(8)]
        print(tabulate(table, headers = header, tablefmt = 'fancy_grid'))
        print()

    def cell_to_str(self, cell):
        if cell == EMPTY:
            return '.'
        elif cell == BLACK:
            return 'B'
        elif cell == WHITE:
            return 'W'