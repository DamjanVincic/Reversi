import time
import copy
from models.state import State
from models.player import Player

class Computer(object):
    def __init__(self):
        self._transposition_table = {}


    def get_best_move_within_time_limit(self, state: State, time_limit):
        start_time = time.time()
        depth = 3
        best_move = None

        while True:
            try:
                move = self.find_best_move(state, depth, start_time, time_limit)
            except TimeoutError:
                break
            best_move = move
            depth += 1
        return best_move
    
    def find_best_move(self, state: State, depth, start_time, time_limit):
        best_value = float("inf")
        best_move = None

        for move in state.get_valid_moves():
            state_copy = copy.deepcopy(state)
            state_copy.make_move(move)
            value = self.minimax(state_copy, depth-1, True, float("-inf"), float("inf"), start_time, time_limit)
            if value <= best_value:
                best_value = value
                best_move = move
            if time.time() - start_time > time_limit:
                break
        return best_move
    
    def minimax(self, state: State, depth, maximizing_player, alpha, beta, start_time, time_limit):
        board_hash = state.hash_board()
        if board_hash in self._transposition_table and self._transposition_table[board_hash]['depth'] >= depth:
            return self._transposition_table[board_hash]['value']

        if time.time() - start_time > time_limit:
            raise TimeoutError

        valid_moves = state.get_valid_moves()
        if len(valid_moves) == 0:
            black_score, white_score = state.get_score()
            value = None
            if black_score > white_score:
                if maximizing_player:
                    value = float("inf") if state.player == Player.BLACK else float("-inf")
                else:
                    value = float("-inf") if state.player == Player.BLACK else float("inf")
            elif black_score < white_score:
                if maximizing_player:
                    value = float("-inf") if state.player == Player.BLACK else float("inf")
                else:
                    value = float("inf") if state.player == Player.BLACK else float("-inf")
            if value:
                self._transposition_table[board_hash] = {'value': value, 'depth': depth}
                return value

        if depth == 0 or len(valid_moves) == 0:
            opponent = Player.WHITE if state.player == Player.BLACK else Player.BLACK

            if maximizing_player:
                evaluation = state.evaluate()
            else:
                opponent_state = copy.deepcopy(state)
                opponent_state.player = opponent
                evaluation = opponent_state.evaluate()
            
            self._transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
            return evaluation

        if maximizing_player:
            max_value = float("-inf")
            for move in valid_moves:
                state_copy = copy.deepcopy(state)
                state_copy.make_move(move)
                value = self.minimax(state_copy, depth-1, False, alpha, beta, start_time, time_limit)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            self._transposition_table[board_hash] = {'value': max_value, 'depth': depth}
            return max_value
        else:
            min_value = float("inf")
            for move in valid_moves:
                state_copy = copy.deepcopy(state)
                state_copy.make_move(move)
                value = self.minimax(state_copy, depth-1, True, alpha, beta, start_time, time_limit)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            self._transposition_table[board_hash] = {'value': min_value, 'depth': depth}
            return min_value
        
    