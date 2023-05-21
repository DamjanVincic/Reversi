from tabulate import tabulate
from models.player import Player
from models.state import State
from models.computer import Computer


def start_game():
    state = State()
    computer = Computer()
    
    while True:
        valid_moves = state.get_valid_moves()
        if len(valid_moves) == 0:
            break
        
        if state.player == Player.BLACK:
            valid_moves = {k:v for k, v in enumerate(valid_moves, start = 1)}
            state.print_board()

            try:
                choice = int(input("Enter a choice: "))
            except Exception as e:
                pass
            
            while choice not in valid_moves:
                print("Invalid move.")
                try:
                    choice = int(input("Enter a choice: "))
                except Exception as e:
                    pass

            state.make_move(valid_moves[choice])
        elif state.player == Player.WHITE:
            state.print_board()
            row, col = computer.get_best_move_within_time_limit(state, 3)
            print(f"{state.player.name} plays: {chr(ord('A') + col)}{row+1}")
            
            state.make_move((row, col))
    
    state.print_board()

    black_score, white_score = state.get_score()
    print("Game Over!")
    print("-----")
    print("Final Score")
    print(tabulate([state.get_score()], headers = ['○', '●'], tablefmt = 'fancy_grid'))
    print("-----")
    if black_score > white_score:
        print("Black wins!")
    elif black_score < white_score:
        print("White wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    start_game()