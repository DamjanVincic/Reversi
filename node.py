class Node(object):
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.children = []
        self.move = None # Move that led to this board state
        self.value = None