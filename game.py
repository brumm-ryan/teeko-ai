import random
import sys

import numpy as np
import copy
import os


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    # board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self, board):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        # self.my_piece = random.choice(self.pieces)
        # self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.my_piece = 'r'
        self.opp = 'b'
        self.board = board

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        count = 0
        drop_phase = False  # TODO: detect drop phase
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    count += 1
        if count < 8:
            drop_phase = True

        # TODO: implement a minimax algorithm to play better
        # print('getting max state')
        depth = 0
        if drop_phase:
            depth = 2
        max_state = self.max_value(state, depth)
        # print('found max state')
        newRow = -1
        newCol = -1
        oldRow = -1
        oldCol = -1
        for i in range(5):
            for j in range(5):
                if max_state[i][j] == self.my_piece and state[i][j] == ' ':
                    newRow = i
                    newCol = j
                if max_state[i][j] == ' ' and state[i][j] == self.my_piece:
                    oldRow = i
                    oldCol = j

        move = list()
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.append((newRow, newCol))
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move.append((oldRow, oldCol))
            pass

        return move

    # get the max value recursively
    def max_value(self, state, depth):
        if depth == 3 or self.game_value(state) != 0:
            return state
        else:
            succ_list = self.succ(state)
            max_value = -10
            max_index = -1
            max_state = None
            for i in range(len(succ_list)):
                value = self.heuristic_game_value(self.min_value(succ_list[i], depth + 1))
                if value > max_value:
                    max_value = value
                    max_index = i
                    max_state = succ_list[i]
        return max_state

    # get the min value based off opponent
    def min_value(self, state, depth):
        if depth == 3 or self.game_value(state) != 0:
            return state
        else:
            succ_list = self.opp_succ(state)
            min_value = 10
            min_index = -1
            min_state = None
            for i in range(len(succ_list)):
                value = self.heuristic_game_value(self.max_value(succ_list[i], depth + 1))
                if value < min_value:
                    min_value = value
                    min_index = i
                    min_state = succ_list[i]
        return min_state

    def succ(self, state):
        count = 0
        drop_phase = True
        succ_list = list()
        piece_list = list()
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == self.my_piece:
                    count += 1
                    piece_list += [i, j]
        if count == 4:
            drop_phase = False

        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_board = copy.deepcopy(state)
                        new_board[i][j] = self.my_piece
                        succ_list.append(new_board)
        else:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        oldRow = -1
                        oldCol = -1
                        valid_move = False
                        if i > 0 and state[i - 1][j] == self.my_piece:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j
                        elif i < 4 and state[i + 1][j] == self.my_piece:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j
                        elif j > 0 and state[i][j - 1] == self.my_piece:
                            valid_move = True
                            oldRow = i
                            oldCol = j - 1
                        elif j < 4 and state[i][j + 1] == self.my_piece:
                            valid_move = True
                            oldRow = i
                            oldCol = j + 1
                        elif i > 0 and j > 0 and state[i - 1][j - 1] == self.my_piece:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j - 1
                        elif i < 4 and j < 4 and state[i + 1][j + 1] == self.my_piece:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j + 1
                        elif i < 4 and j > 0 and state[i + 1][j - 1] == self.my_piece:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j - 1
                        elif i > 0 and j < 4 and state[i - 1][j + 1] == self.my_piece:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j + 1
                        if valid_move:
                            new_board = copy.deepcopy(state)
                            new_board[i][j] = self.my_piece
                            new_board[oldRow][oldCol] = ' '
                            succ_list.append(new_board)
        return succ_list

    def opp_succ(self, state):
        count = 0
        drop_phase = True
        succ_list = list()
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == self.opp:
                    count += 1
        if count == 4:
            drop_phase = False

        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_board = copy.deepcopy(state)
                        new_board[i][j] = self.opp
                        succ_list.append(new_board)
        else:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        oldRow = -1
                        oldCol = -1
                        valid_move = False
                        if i > 0 and state[i - 1][j] == self.opp:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j
                        elif i < 4 and state[i + 1][j] == self.opp:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j
                        elif j > 0 and state[i][j - 1] == self.opp:
                            valid_move = True
                            oldRow = i
                            oldCol = j - 1
                        elif j < 4 and state[i][j + 1] == self.opp:
                            valid_move = True
                            oldRow = i
                            oldCol = j + 1
                        elif i > 0 and j > 0 and state[i - 1][j - 1] == self.opp:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j - 1
                        elif i < 4 and j < 4 and state[i + 1][j + 1] == self.opp:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j + 1
                        elif i < 4 and j > 0 and state[i + 1][j - 1] == self.opp:
                            valid_move = True
                            oldRow = i + 1
                            oldCol = j - 1
                        elif i > 0 and j < 4 and state[i - 1][j + 1] == self.opp:
                            valid_move = True
                            oldRow = i - 1
                            oldCol = j + 1
                        if valid_move:
                            new_board = copy.deepcopy(state)
                            new_board[i][j] = self.opp
                            new_board[oldRow][oldCol] = ' '
                            succ_list.append(new_board)
        return succ_list

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def heuristic_game_value(self, state):
        is_terminal = self.game_value(state)
        if is_terminal != 0:
            return is_terminal
        my_score = 0
        opp_score = 0
        # count the horizontal 2 in a row placements
        for i in range(5):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j + 1]:
                    if state[i][j] == self.my_piece:
                        my_score += 1
                    else:
                        opp_score += 1
        # count the vertical 2 in a row placements
        for i in range(4):
            for j in range(5):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j]:
                    if state[i][j] == self.my_piece:
                        my_score += 1
                    else:
                        opp_score += 1
        # count the horizontal 3 in a row placements
        for i in range(5):
            for j in range(3):
                if state[i][j] != ' ' and state[i][j] == state[i][j + 1] == state[i][j + 2]:
                    if state[i][j] == self.my_piece:
                        my_score += 6
                    else:
                        opp_score += 6
                # block opponents chance at 3 in a row
                if state[i][j] != ' ' and state[i][j] == state[i][j + 1] == self.opp and state[i][
                    j + 2] == self.my_piece:
                    my_score += 3
        # count the vertical 3 in a row placements
        for i in range(3):
            for j in range(5):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == state[i + 2][j]:
                    if state[i][j] == self.my_piece:
                        my_score += 6
                    else:
                        opp_score += 6
                # block opponents chance at 3 in a row slightly less than build my own 3
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == self.opp and state[i + 2][
                    j] == self.my_piece:
                    my_score += 3
        # get all the diags and look for rows of three and two
        np_state = np.array(state)
        diags = [np_state[::-1, :].diagonal(i) for i in range(-np_state.shape[0] + 1, np_state.shape[1])]
        diags.extend(np_state.diagonal(i) for i in range(np_state.shape[1] - 1, -np_state.shape[0], -1))
        for d in diags:
            if len(d) >= 4:
                for i in range(0, len(d) - 2):
                    if d[i] != ' ' and d[i] == d[i + 1] == d[i + 2]:
                        if d[i] == self.my_piece:
                            my_score += 6
                        else:
                            opp_score += 6
                    if d[i] != ' ' and d[i] == d[i + 1] == self.opp and state[i + 2][
                        j] == self.my_piece:
                        my_score += 3

                for i in range(0, len(d) - 1):
                    if d[i] != ' ' and d[i] == d[i + 1]:
                        if d[i] == self.my_piece:
                            my_score += 1
                        else:
                            opp_score += 1
            else:
                continue

        for i in range(len(state) - 2):
            for j in range(len(state) - 2):
                if state[i][j] != ' ' and (state[i][j] == state[i + 2][j] or state[i][j] == state[i][j + 2]
                                           or state[i][j] == state[i + 2][j + 2]):
                    if state[i][j] == self.my_piece:
                        my_score += 1
                    else:
                        opp_score += 1
                if state[i][j] != ' ' and (state[i][j] == state[i + 2][j] == state[i][j + 2]
                                           or state[i][j] == state[i + 2][j] == state[i + 2][j + 2]):
                    if state[i][j] == self.my_piece:
                        my_score += 3
                    else:
                        opp_score += 3

        # return a normalized value that will be between - 1 and 1 representing the value of the board
        return (my_score - opp_score) / (my_score + opp_score + 1)

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1
        # TODO: check \ diagonal wins
        # TODO: check / diagonal wins
        winning_diagonal = list()
        np_state = np.array(state)
        diags = [np_state[::-1, :].diagonal(i) for i in range(-np_state.shape[0] + 1, np_state.shape[1])]
        diags.extend(np_state.diagonal(i) for i in range(np_state.shape[1] - 1, -np_state.shape[0], -1))
        for d in diags:
            diagonalWin = True
            # skip all diags that are less than 4
            if len(d) < 4:
                continue
            # for the middle diag of length 5, break into two sub diags both of len 4
            if len(d) == 5:
                diags.append(d[0:len(d) - 1])
                diags.append(d[1:len(d)])
            # iterate through diag and check if consecutive elements are the same
            for i in range(len(d) - 1):
                # if two consecutive elements are different there can't be a diag win
                if d[i] != d[i + 1]:
                    diagonalWin = False
            #
            if diagonalWin:
                winning_diagonal = d
                if winning_diagonal[0] != ' ':
                    return 1 if winning_diagonal[0] == self.my_piece else -1
        # TODO: check 3x3 square corners wins
        for i in range(len(state) - 2):
            for j in range(len(state) - 2):
                if state[i][j] != ' ' and state[i][j] == state[i + 2][j] == state[i][j + 2] == state[i + 2][j + 2]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
