from tabulate import tabulate
import random
import copy
from models.player import Player

class State(object):
    def __init__(self):
        self._board = [[Player.EMPTY]*8 for _ in range(8)]
        self._board[3][3] = Player.BLACK
        self._board[3][4] = Player.WHITE
        self._board[4][3] = Player.WHITE
        self._board[4][4] = Player.BLACK

        self._player = Player.BLACK

        self._directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        self._zobrist_keys = {}
        for i in range(8):
            for j in range(8):
                for player in [Player.BLACK, Player.WHITE]:
                    self._zobrist_keys[(i, j, player)] = random.getrandbits(64)
        self._black_turn_to_play = random.getrandbits(64)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player


    def print_board(self, valid_moves: dict = None):
        header = [chr(ord('A') + col) for col in range(8)]
        if self._player == Player.BLACK:
            table = []
            valid_moves = {k:v for k, v in enumerate(self.get_valid_moves(), start = 1)}
            for i in range(8):
                row = [str(i+1)]
                for j in range(8):
                    found = False
                    for k, v in valid_moves.items():
                        if v == (i, j):
                            row.append(k)
                            found = True
                            break
                    if not found:
                        row.append(self.cell_to_str(self._board[i][j]))
                table.append(row)
                    
        else:
            table = [[str(i+1)] + [self.cell_to_str(self._board[i][j]) for j in range(8)] for i in range(8)]
        print(tabulate(table, headers = header, tablefmt = 'fancy_grid'))
        print()

    def cell_to_str(self, cell):
        if cell == Player.EMPTY:
            return ' '
        elif cell == Player.BLACK:
            return '○'
        elif cell == Player.WHITE:
            return '●'
        
    def get_score(self):
        black_score = white_score = 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == Player.BLACK:
                    black_score += 1
                elif self._board[i][j] == Player.WHITE:
                    white_score += 1
        return black_score, white_score
    
    def get_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == Player.EMPTY and self.is_valid_move((i, j)):
                    valid_moves.append((i, j))
        return valid_moves
    
    def is_valid_move(self, move):
        i, j = move
        if self._board[i][j] != Player.EMPTY:
            return False

        opponent = Player.WHITE if self._player == Player.BLACK else Player.BLACK
        for direction in self._directions:
            di, dj = direction
            new_i, new_j = i + di, j + dj

            if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
                continue
            
            if self._board[new_i][new_j] == opponent:
                while True:
                    new_i += di
                    new_j += dj
                    if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
                        break
                    if self._board[new_i][new_j] == Player.EMPTY:
                        break
                    if self._board[new_i][new_j] == self._player:
                        return True
        return False
    
    def make_move(self, move):
        i, j = move
        self._board[i][j] = self._player
        opponent = Player.WHITE if self._player == Player.BLACK else Player.BLACK

        for direction in self._directions:
            di, dj = direction
            new_i, new_j = i + di, j + dj

            if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
                continue

            if self._board[new_i][new_j] == opponent:
                positions_to_flip = []
                while 0 <= new_i <= 7 and 0 <= new_j <= 7:
                    if self._board[new_i][new_j] == Player.EMPTY:
                        break
                    if self._board[new_i][new_j] == self._player:
                        for position in positions_to_flip:
                            pos_i, pos_j = position
                            self._board[pos_i][pos_j] = self._player
                        break
                    positions_to_flip.append((new_i, new_j))
                    new_i += di
                    new_j += dj

        self._player = opponent

    def hash_board(self):
        board_hash = 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] != Player.EMPTY:
                    board_hash ^= self._zobrist_keys[(i, j, self._board[i][j])]
        if self._player == Player.BLACK:
            board_hash ^= self._black_turn_to_play
        return board_hash
    
    def evaluate(self):
        opponent = Player.WHITE if self._player == Player.BLACK else Player.BLACK
        player_tiles = opponent_tiles = player_front_tiles = opponent_front_tiles = 0
        d = 0

        weigths = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]

        for i in range(8):
            for j in range(8):
                if self._board[i][j] == self._player:
                    d += weigths[i][j]
                    player_tiles += 1
                elif self._board[i][j] == opponent:
                    d -= weigths[i][j]
                    opponent_tiles += 1

                if self._board[i][j] != Player.EMPTY:
                    for direction in self._directions:
                        x = i + direction[0]
                        y = j + direction[1]
                        if 0 <= x <= 7 and 0 <= y <= 7 and self._board[x][y] == Player.EMPTY:
                            if self._board[i][j] == self._player:
                                player_front_tiles += 1
                            else:
                                opponent_front_tiles += 1
                            break
        

        if player_tiles > opponent_tiles:
            p = (100.0 * player_tiles) / (player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            p = -(100.0 * opponent_tiles) / (player_tiles + opponent_tiles)
        else:
            p = 0

        if player_front_tiles > opponent_front_tiles:
            f = -(100.0 * player_front_tiles) / (player_front_tiles + opponent_front_tiles)
        elif player_front_tiles < opponent_front_tiles:
            f = (100.0 * opponent_front_tiles) / (player_front_tiles + opponent_front_tiles)
        else:
            f = 0


        player_tiles = opponent_tiles = 0
        for i in [0, 7]:
            for j in [0, 7]:
                if self._board[i][j] == self._player:
                    player_tiles += 1
                elif self._board[i][j] == opponent:
                    opponent_tiles += 1
        c = 25 * (player_tiles - opponent_tiles)


        corner_closeness = [
            (0, 0, [(0, 1), (1, 1), (1, 0)]),
            (0, 7, [(0, 6), (1, 6), (1, 7)]),
            (7, 0, [(6, 0), (6, 1), (7, 1)]),
            (7, 7, [(6, 7), (6, 6), (7, 6)])
        ]

        player_tiles = opponent_tiles = 0

        for x, y, adjacent_tiles in corner_closeness:
            if self._board[x][y] == Player.EMPTY:
                for adj_x, adj_y in adjacent_tiles:
                    if self._board[adj_x][adj_y] == self._player:
                        player_tiles += 1
                    elif self._board[adj_x][adj_y] == opponent:
                        opponent_tiles += 1
        l = -12.5 * (player_tiles - opponent_tiles)


        player_valid_moves = len(self.get_valid_moves())

        opponent_state = copy.deepcopy(self)
        opponent_state.player = opponent

        opponent_valid_moves = len(opponent_state.get_valid_moves())
        
        if player_valid_moves > opponent_valid_moves:
            m = (100.0 * player_valid_moves) / (player_valid_moves + opponent_valid_moves)
        elif player_valid_moves < opponent_valid_moves:
            m = -(100.0 * opponent_valid_moves) / (player_valid_moves + opponent_valid_moves)
        else:
            m = 0

        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
        return score