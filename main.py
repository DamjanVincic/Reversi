from tabulate import tabulate

EMPTY = 0
BLACK = 1
WHITE = 2

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def is_valid_move(board, player, move):
    i, j = move
    if board[i][j] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK
    for direction in directions:
        di, dj = direction
        new_i, new_j = i + di, j + dj

        if new_i > 7 or new_i < 0 or new_j > 7 or new_j < 0:
            return False
        
        if board[new_i][new_j] == opponent:
            while 0 <= new_i <= 7 and 0 <= new_j <= 7:
                if board[new_i][new_j] == EMPTY:
                    break
                elif board[new_i][new_j] == player:
                    return True
                new_i += di
                new_j += dj
    return False

def get_valid_moves(board, player):
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == EMPTY and is_valid_move(board, player, (i, j)):
                valid_moves.append((i, j))
    return valid_moves

def make_move(board, player, move):
    i, j = move
    board[i][j] = player
    opponent = WHITE if player == BLACK else BLACK

    for direction in directions:
        di, dj = direction
        new_i, new_j = i + di, j + dj

        if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
            continue

        if board[new_i][new_j] == opponent:
            positions_to_flip = []
            while 0 <= new_i <= 7 and 0 <= new_j <= 7:
                if board[new_i][new_j] == EMPTY:
                    break
                if board[new_i][new_j] == player:
                    for position in positions_to_flip:
                        pos_i, pos_j = position
                        board[pos_i][pos_j] = player
                    break
                positions_to_flip.append((new_i, new_j))
                new_i += di
                new_j += dj
    return board


def cell_to_str(cell):
    if cell == EMPTY:
        return '.'
    elif cell == BLACK:
        return 'B'
    elif cell == WHITE:
        return 'W'

def print_board(board, valid_moves):
    header = [str(col) for col in range(8)]
    table = [[str(i)] + [cell_to_str(board[i][j]) if (i, j) not in valid_moves else '?' for j in range(8)] for i in range(8)]
    print(tabulate(table, headers = header, tablefmt = 'fancy_grid'))
    print()


def start_game():
    board = [[EMPTY]*8 for _ in range(8)]
    board[3][3] = BLACK
    board[3][4] = WHITE
    board[4][3] = WHITE
    board[4][4] = BLACK

    current_player = BLACK

    
    while True:
        if current_player == BLACK:
            valid_moves = get_valid_moves(board, current_player)
            if len(valid_moves) == 0:
                break

            print_board(board, valid_moves)

            try:
                row, col = map(int, input("Enter row and col: ").split())
            except Exception as e:
                print("Invalid move.")
            
            while (row, col) not in valid_moves:
                print("Invalid move.")
                try:
                    row, col = map(int, input("Enter row and col: ").split())
                except Exception as e:
                    pass
            
            board = make_move(board, current_player, (row, col))
            current_player = WHITE
        elif current_player == WHITE:
            valid_moves = get_valid_moves(board, current_player)
            if len(valid_moves) == 0:
                break

            print_board(board, valid_moves)

            try:
                row, col = map(int, input("Enter row and col: ").split())
            except Exception as e:
                print("Invalid move.")
            
            while (row, col) not in valid_moves:
                print("Invalid move.")
                try:
                    row, col = map(int, input("Enter row and col: ").split())
                except Exception as e:
                    pass
            
            board = make_move(board, current_player, (row, col))
            current_player = BLACK
        
        # print_board(board, valid_moves)


    # print_board(board, valid_moves)

if __name__ == "__main__":
    start_game()