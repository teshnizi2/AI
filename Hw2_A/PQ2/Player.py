from Board import BoardUtility
import random
import copy


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        pass


class RandomPlayer(Player):
    def play(self, board):
        valid_locations = BoardUtility.get_valid_locations(board)
        location = random.choice(valid_locations)
        rotation = random.choice([1, 2, 3, 4])
        action = random.choice(["skip", "clockwise", "anticlockwise"])
        return [location, rotation, action]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n").split()
        location = [int(move[0]), int(move[1])]
        rotation = int(move[2])
        action = move[3]
        return [location, rotation, action]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def play(self, board):
        _, best_move = self.max_play(board, self.depth, self.piece)
        return best_move

    def max_play(self, board, depth, piece):
        if depth == 0:
            return BoardUtility.score_position(board, piece), None

        locs = BoardUtility.get_valid_locations(board)
        best_move = None
        best_value = float('-inf')

        for loc in locs:
            for action in ["skip", "clockwise", "anticlockwise"]:
                for rotation in range(1, 5):
                    temp_board = copy.deepcopy(board)
                    BoardUtility.make_move(temp_board, loc[0], loc[1], rotation, action, piece)
                    value, _ = self.min_play(temp_board, depth - 1, 3 - piece)
                    if value > best_value:
                        best_value = value
                        best_move = [loc, rotation, action]
                    if action == 'skip':
                        break

        return best_value, best_move

    def min_play(self, board, depth, piece):
        if depth == 0:
            return BoardUtility.score_position(board, piece), None

        locs = BoardUtility.get_valid_locations(board)
        best_move = None
        best_value = float('inf')

        for loc in locs:
            for action in ["skip", "clockwise", "anticlockwise"]:
                for rotation in range(1, 5):
                    temp_board = copy.deepcopy(board)
                    BoardUtility.make_move(temp_board, loc[0], loc[1], rotation, action, piece)
                    value, _ = self.max_play(temp_board, depth - 1, 3 - piece)
                    if value < best_value:
                        best_value = value
                        best_move = [loc, rotation, action]
                    if action == 'skip':
                        break

        return best_value, best_move


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def play(self, board):
        _, best_move = self.max_play(board, self.depth, self.piece)
        return best_move

    def max_play(self, board, depth, piece):
        if depth == 0:
            return BoardUtility.score_position(board, piece), None

        locs = BoardUtility.get_valid_locations(board)
        best_move = None
        best_value = float('-inf')
        moves = []
        values = []

        for loc in locs:
            for action in ["skip", "clockwise", "anticlockwise"]:
                for rotation in range(1, 5):
                    temp_board = copy.deepcopy(board)
                    BoardUtility.make_move(temp_board, loc[0], loc[1], rotation, action, piece)
                    value, _ = self.min_play(temp_board, depth - 1, 3 - piece)
                    moves.append([loc, rotation, action])
                    values.append(value)
                    if value > best_value:
                        best_value = value
                        best_move = [loc, rotation, action]
                    if action == 'skip':
                        break

        if random.random() < self.prob_stochastic:
            i = random.randint(0, len(moves) - 1)
            return values[i], moves[i]

        return best_value, best_move

    def min_play(self, board, depth, piece):
        if depth == 0:
            return BoardUtility.score_position(board, piece), None

        locs = BoardUtility.get_valid_locations(board)
        best_move = None
        best_value = float('inf')

        for loc in locs:
            for action in ["skip", "clockwise", "anticlockwise"]:
                for rotation in range(1, 5):
                    temp_board = copy.deepcopy(board)
                    BoardUtility.make_move(temp_board, loc[0], loc[1], rotation, action, piece)
                    value, _ = self.max_play(temp_board, depth - 1, 3 - piece)
                    if value < best_value:
                        best_value = value
                        best_move = [loc, rotation, action]
                    if action == 'skip':
                        break

        return best_value, best_move
