# Author: YUN EN TSAI
# GitHub username: somebody1997
# Description: Write a cheese board game, use make_move to play the cheese, the program will check for each type of
# cheese state. If any color of type cheese are all captured, then the player win the game.
# EX: move_result = game.make_move('a2', 'a4'), print(from_square, to_square)

class ChessVar:
    def __init__(self):
        '''
        init board size, set first white turn, set game state and set captured pieces to count for captured cheese
        call init_pieces
        '''
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.turn = 'WHITE'  # init the first hand - white hand
        self.game_state = 'UNFINISHED'
        self.captured_pieces = {'WHITE': [], 'BLACK': []}

        self.place_init_pieces()

    def place_init_pieces(self):
        '''
        :return: return an init fresh new cheese board
        '''
        for col in range(8):
            self.board[1][col] = 'P' # Black
            self.board[6][col] = 'p' # White

        place_piece = 'RNBQKBNR'
        for col, piece in enumerate(place_piece):  # use enumerate fun to fill the board place
            self.board[0][col] = piece
            self.board[7][col] = piece.lower()

    def get_game_state(self):
        '''
        :return: return the game state, 'WHITE_WON', 'BLACK_WON' or 'UNFINISHED'
        '''
        return self.game_state

    def make_move(self, from_square, to_square):
        '''
        :param from_square: start place on cheese board
        :param to_square:   place want to go on cheese board
        :return:    return True for all move and capture are correct
        '''
        if self.game_state != 'UNFINISHED':
            return False

        from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

        # is_valid_move will return true for checking correct move and capture
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False

        # Capture the piece if present
        captured_piece = self.board[to_row][to_col]
        if captured_piece:
            self.captured_pieces['WHITE' if captured_piece.islower() else 'BLACK'].append(captured_piece)

        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ''

        self.check_game_state()  # check for winning
        self.turn = 'BLACK' if self.turn == 'WHITE' else 'WHITE'
        return True

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return: check for correct move on cheese board, return False for wrong turn, move and capture, else return True
        '''
        moving_piece = self.board[from_row][from_col]
        target_piece = self.board[to_row][to_col]

        # check white black turn
        if (self.turn == 'WHITE' and moving_piece.isupper()) or \
                (self.turn == 'BLACK' and moving_piece.islower()):
            return False

        #check for right capture
        if target_piece and ((self.turn == 'WHITE' and target_piece.islower()) or
                             (self.turn == 'BLACK' and target_piece.isupper())):
            return False

        if moving_piece.lower() == 'p':  # Pawn
            return self.check_pawn_move(from_row, from_col, to_row, to_col, target_piece)
        elif moving_piece.lower() == 'r':  # Rookcheck_pawn_move
            return self.check_rook_move(from_row, from_col, to_row, to_col)
        elif moving_piece.lower() == 'n':  # Knight
            return self.check_knight_move(from_row, from_col, to_row, to_col)
        elif moving_piece.lower() == 'b':  # Bishop
            return self.check_bishop_move(from_row, from_col, to_row, to_col)
        elif moving_piece.lower() == 'q':  # Queen
            return self.check_queen_move(from_row, from_col, to_row, to_col)
        elif moving_piece.lower() == 'k':  # King
            return self.check_king_move(from_row, from_col, to_row, to_col)

        return True

    def check_pawn_move(self, from_row, from_col, to_row, to_col, target_piece):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :param target_piece: target place on cheese board
        :return:    return check for pawn move, at init move(1 step or 2 steps), and pawn capture correct or not
        '''
        move_direction = -1 if self.turn == 'WHITE' else 1

        if from_col == to_col:
            if (self.turn == 'WHITE' and from_row == 6) or (self.turn == 'BLACK' and from_row == 1):
                if to_row == (from_row + 2 * move_direction) and \
                                self.board[from_row + move_direction][from_col] == '' and target_piece == '':
                    return True

        if from_col == to_col and to_row == from_row + move_direction and target_piece == '':
            return True

        if abs(from_col - to_col) == 1 and to_row == from_row + move_direction:
            if target_piece and ((self.turn == 'WHITE' and target_piece.isupper()) or (self.turn == 'BLACK' and
                                                                                       target_piece.islower())):
                return True  # Diagonal capture

        return False

    def check_rook_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:    return check for rook move both row and col
        '''
        if from_row != to_row and from_col != to_col:
            return False

        if from_row == to_row:
            start, end = sorted([from_col, to_col])
            for col in range(start + 1, end):
                if self.board[from_row][col] != '':
                    return False
        else:
            start, end = sorted([from_row, to_row])
            for row in range(start + 1, end):
                if self.board[row][from_col] != '':
                    return False

        return True

    def check_knight_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:    return True for move w steps row or col and one-step row or col after
        '''
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True

    def check_bishop_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:    check bishop's move, return false for moving straight or row
        '''
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False

        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1

        current_row, current_col = from_row + row_step, from_col + col_step

        while current_row != to_row and current_col != to_col:
            if self.board[current_row][current_col] != '':
                return False

            current_row += row_step
            current_col += col_step

        return True

    def check_queen_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:    check for queen's move both col and row
        '''
        if from_row == to_row or from_col == to_col:
            return self.check_path_clear(from_row, from_col, to_row, to_col)

            # Diagonal move (like a bishop)
        if abs(from_row - to_row) == abs(from_col - to_col):
            return self.check_path_clear(from_row, from_col, to_row, to_col)

        return False

    def check_path_clear(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:   True or False for the path is clean to let Queen move, any cheese on the way will stop her
        '''
        row_step = 1 if to_row > from_row else -1 if to_row < from_row else 0
        col_step = 1 if to_col > from_col else -1 if to_col < from_col else 0

        current_row, current_col = from_row, from_col

        while (current_row, current_col) != (to_row, to_col):
            current_row += row_step
            current_col += col_step

            if (current_row, current_col) == (to_row, to_col):
                break

            if self.board[current_row][current_col] != '':
                return False

        return True

    def check_king_move(self, from_row, from_col, to_row, to_col):
        '''
        :param from_row: row of the move cheese on the board
        :param from_col: col of the move cheese on the board
        :param to_row:   row of the place where want to go
        :param to_col:   col of the place where want to go
        :return:    True or False for checking kings diff movement and capture
        '''
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)

        # Check if the move is either one square horizontally, vertically, or diagonally
        if not (row_diff == 1 and col_diff <= 1) or (col_diff == 1 and row_diff <= 1):
            return False

        return True

    def check_game_state(self):
        '''
        check for game state, if any type of one color of cheese been caputerd all, set the game state
        return: game state
        '''
        for player, pieces in self.captured_pieces.items():
            if pieces.count('P' if player == 'BLACK' else 'p') == 8 or \
                    pieces.count('N' if player == 'BLACK' else 'n') == 2 or \
                    pieces.count('B' if player == 'BLACK' else 'b') == 2 or \
                    pieces.count('R' if player == 'BLACK' else 'r') == 2 or \
                    pieces.count('Q' if player == 'BLACK' else 'q') == 1 or \
                    pieces.count('K' if player == 'BLACK' else 'k') >= 1:
                self.game_state = 'WHITE_WON' if player == 'BLACK' else 'BLACK_WON'

    def print_board(self):
        '''
        :return: return the cheese board
        '''
        for row in self.board:
            print(' '.join(row))
        print()
