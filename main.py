from tabulate import tabulate
import copy
from node import Node

EMPTY = 0
BLACK = 1
WHITE = 2

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def evaluate(board, player):
    opponent = WHITE if player == BLACK else BLACK
    player_tiles = opponent_tiles = player_front_tiles = opponent_front_tiles = 0
    # d = p = f = c = l = m = 0
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
            if board[i][j] == player:
                d += weigths[i][j]
                player_tiles += 1
            elif board[i][j] == opponent:
                d -= weigths[i][j]
                opponent_tiles += 1

            if board[i][j] != EMPTY:
                for direction in directions:
                    x = i + direction[0]
                    y = j + direction[1]
                    if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == EMPTY:
                        if board[i][j] == player:
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
            if board[i][j] == player:
                player_tiles += 1
            elif board[i][j] == opponent:
                opponent_tiles += 1
    c = 25 * (player_tiles - opponent_tiles)


    corner_closeness = [
        (0, 0, [(0, 1), (1, 1), (1, 0)]),
        (0, 7, [(0, 6), (1, 6), (1, 7)]),
        (7, 0, [(6, 0), (6, 1), (7, 1)]),
        (7, 7, [(6, 7), (6, 6), (7, 6)])
    ]

    # my_corner_tiles = 0
    # opp_corner_tiles = 0
    player_tiles = opponent_tiles = 0

    for x, y, adjacent_tiles in corner_closeness:
        if board[x][y] == EMPTY:
            for adj_x, adj_y in adjacent_tiles:
                if board[adj_x][adj_y] == player:
                    player_tiles += 1
                elif board[adj_x][adj_y] == opponent:
                    opponent_tiles += 1
    l = -12.5 * (player_tiles - opponent_tiles)


    player_valid_moves = len(get_valid_moves(board, player))
    opponent_valid_moves = len(get_valid_moves(board, opponent))
    
    if player_valid_moves > opponent_valid_moves:
        m = (100.0 * player_valid_moves) / (player_valid_moves + opponent_valid_moves)
    elif player_valid_moves < opponent_valid_moves:
        m = -(100.0 * opponent_valid_moves) / (player_valid_moves + opponent_valid_moves)
    else:
        m = 0

    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score


def generate_game_tree(board, player, depth):
    node = Node(board, player)
    if depth == 0 or len(get_valid_moves(board, player)) == 0:
        node.value = evaluate(board, player)
        return node

    valid_moves = get_valid_moves(board, player)
    for move in valid_moves:
        new_board = make_move(copy.deepcopy(board), player, move)
        child_node = generate_game_tree(new_board, WHITE if player == BLACK else BLACK, depth - 1)
        child_node.move = move
        node.children.append(child_node)

    return node


def minimax(node, depth, maximizing_player, alpha, beta):
    if depth == 0 or len(node.children) == 0:
        return node.value

    if maximizing_player:
        max_value = float("-inf")
        for child in node.children:
            value = minimax(child, depth-1, False, alpha, beta)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_value
    else:
        min_value = float("inf")
        for child in node.children:
            value = minimax(child, depth-1, True, alpha, beta)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_value


def find_best_move(board, player, depth):
    game_tree = generate_game_tree(board, player, depth)
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for child in game_tree.children:
        value = minimax(child, depth-1, False, alpha, beta)
        if value > best_score:
            best_score = value
            best_move = child.move

    return best_move


def is_valid_move(board, player, move):
    i, j = move
    if board[i][j] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK
    for direction in directions:
        di, dj = direction
        new_i, new_j = i + di, j + dj

        if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
            continue
        
        if board[new_i][new_j] == opponent:
            while True:
                new_i += di
                new_j += dj
                if not (0 <= new_i <= 7 and 0 <= new_j <= 7):
                    break
                if board[new_i][new_j] == EMPTY:
                    break
                if board[new_i][new_j] == player:
                    return True
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


def get_score(board):
    black_score = white_score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == BLACK:
                black_score += 1
            elif board[i][j] == WHITE:
                white_score += 1
    return black_score, white_score


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
        valid_moves = get_valid_moves(board, current_player)
        if len(valid_moves) == 0:
            break
        
        if current_player == BLACK:
            print_board(board, valid_moves)

            try:
                row, col = map(int, input("Enter row and col: ").split())
            except Exception as e:
                pass
            
            while (row, col) not in valid_moves:
                print("Invalid move.")
                try:
                    row, col = map(int, input("Enter row and col: ").split())
                except Exception as e:
                    pass
            
            board = make_move(board, current_player, (row, col))
            current_player = WHITE
        elif current_player == WHITE:
            row, col = find_best_move(board, current_player, 4)
            print("WHITE plays:", row, col)
            # make_move(board, row, col, WHITE)

            # best_move = None
            # best_eval = float('-inf')
            # for i, child in enumerate(game_tree.children):
            #     eval_score = minimax(child, 4, False)
            #     if eval_score > best_eval:
            #         best_eval = eval_score
            #         best_move = valid_moves[i]
            
            board = make_move(board, current_player, (row, col))
            current_player = BLACK
        
    black_score, white_score = get_score(board)
    print("Game Over!")
    print("-----")
    print(f"Black score: {black_score}\nWhite Score: {white_score}")
    print("-----")
    if black_score > white_score:
        print("Black wins!")
    elif black_score < white_score:
        print("White wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    start_game()