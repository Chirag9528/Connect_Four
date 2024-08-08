import numpy as np
import math
import copy
import time

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.new_board = np.zeros([6,7]).astype(np.uint8)
        
    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        start = time.time()
        depth = 0
        alpha = -float(math.inf)
        beta = float(math.inf)
        (v , move) = self.max_val(board, depth, alpha, beta )
        end = time.time()
        print("Time : ", end-start) # Testing the Time taken by AI
        return move # Returns the end move taken by AI
        
    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        depth = 0
        alpha = -float(math.inf)
        beta = float(math.inf)
        (v , move) = self.expectimax_val(board, depth, alpha, beta )
        # returning the best move
        return move


    def min_val(self, board, depth, alpha, beta ):
        if depth == 1:
            if self.terminalEval(board)==True: #Checking for the Terminal state
                return math.inf
            
        cost = float(math.inf)

        if depth == 5:
            return self.evaluation_function(board)
        else:
            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board) # Creating the copy of the original Board
                    if self.player_number == 1:
                        self.update_board(i, 2)
                    else:
                        self.update_board(i, 1)
                    new_cost , move = self.max_val(self.new_board, depth+1, alpha, beta) # Calling Max Function

                    if new_cost < cost:  
                        cost = new_cost
                    if cost <= alpha:
                        return cost
                    beta = min(beta, cost) # Updating the beta value
            return cost
                    
    def max_val(self, board, depth, alpha, beta ):
        if depth == 0:
            move2 = -1
            cost2 = -float(math.inf)

            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board)
                    self.update_board(i, self.player_number+2)
                    new_cost = self.terminalEval(self.new_board) # Checking for the terminal state
                    move2 = i
                    if new_cost == True:
                        return cost2 ,move2

        move = -1
        cost = -float(math.inf)

        if depth == 5:
            return self.evaluation_function(board) , move
        else:
            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board)
                    self.update_board(i, self.player_number)
                    new_cost = self.min_val(self.new_board, depth+1, alpha, beta) # Calling the Min Function

                    if new_cost > cost:
                        move = i
                        cost = new_cost
                        if new_cost == math.inf:
                            return cost ,move
                    if cost >= beta:
                        return (cost , move)
                    alpha = max(alpha, cost) # Updating the alpha value
            return (cost , move)
        
    def min_chance(self, board, depth, alpha, beta):
        if depth == 1:
            if self.terminalEval(board)==True:
                return math.inf
            
        if depth == 4:
            return self.evaluation_function(board)
        else:
            average = 0
            size = board.shape[1]
            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board)
                    if self.player_number == 1:
                        self.update_board(i, 2)
                    else:
                        self.update_board(i, 1)
                    new_cost , move = self.expectimax_val(self.new_board, depth+1, alpha, beta) #Calling the expected function
                    average = average + ((1/size)*new_cost)
            return average
    
    def expectimax_val(self, board, depth, alpha, beta):
        if depth == 0:
            move2 = -1
            cost2 = -float(math.inf)
            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board)
                    self.update_board(i, self.player_number+2)
                    new_cost = self.terminalEval(self.new_board)
                    move2 = i
                    if new_cost == True:
                        return cost2 ,move2
        
        move = -1
        cost = -float(math.inf)
        if depth == 4:
            return self.evaluation_function(board) , move
        else:
            for i in range(board.shape[1]):
                if 0 in board[:, i]:
                    self.new_board = copy.deepcopy(board)
                    self.update_board(i, self.player_number)
                    new_cost = self.min_chance(self.new_board, depth+1, alpha, beta)
                    if new_cost > cost:
                        move = i
                        cost = new_cost
                        if new_cost == math.inf:
                            return cost ,move
                    if cost >= beta:
                        return (cost , move)
                    alpha = max(alpha, cost)
            return (cost , move)
    
    def terminalEval(self,board):
        # below are patterns for checking terminal states
        pattern5 = ['{0}{0}{0}3' , '3{0}{0}{0}','{0}3{0}{0}','{0}{0}3{0}']
        pattern6 = ['{0}{0}{0}4' , '4{0}{0}{0}','{0}4{0}{0}','{0}{0}4{0}']
        pattern2 = ['{0}{0}{0}3' , '{0}{0}{0}4' , '3{0}{0}{0}','{0}3{0}{0}','{0}{0}3{0}','{0}{0}4{0}','{0}4{0}{0}','4{0}{0}{0}']
        pattern8 = ['30220','03220' , '00223']
        pattern9 = ['40110','04110','00114']
        if self.player_number == 1:
            player2 = 2
        else:
            player2 = 1
        to_str = lambda a: ''.join(a.astype(str))
        # For checking in horizontal direction 
        for row in board:
            if player2 == 2:
                for i in pattern8:
                    pattern_str = i
                    if pattern_str in to_str(row):
                        return True
            else:
                for i in pattern9:
                    pattern_str = i
                    if pattern_str in to_str(row):
                        return True
        for row in board:
            for i in pattern2:
                pattern_str = i.format(self.player_number)
                if pattern_str in to_str(row):
                    return True
        for row in board:
            if player2 == 2:
                for i in pattern5:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        return True
            else:
                for i in pattern6:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        return True
                    
        # For checking in vertical direction
        for row in board.T:
            if player2 == 2:
                pattern_str = '{0}{0}{0}3'.format(self.player_number)
            else:
                pattern_str = '{0}{0}{0}4'.format(self.player_number)
            if pattern_str in to_str(row):
                return True
        for row in board.T:
            if player2 == 2:
                pattern_str = '3{0}{0}{0}'.format(player2)
                if pattern_str in to_str(row):
                    return True
            else:
                pattern_str = '4{0}{0}{0}'.format(player2)
                if pattern_str in to_str(row):
                    return True

        # For checking in diagonals
        for op in [None, np.fliplr]:
                op_board = op(board) if op else board
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player2 == 2:
                    pattern_str = '{0}{0}{0}3'.format(self.player_number)
                else:
                    pattern_str = '{0}{0}{0}4'.format(self.player_number)
                if pattern_str in to_str(root_diag):
                    return True
                if player2 == 2:
                    for i in pattern5:
                        pattern_str = i.format(player2)
                        if pattern_str in to_str(root_diag):
                            return True
                else:
                    for i in pattern6:
                        pattern_str = i.format(player2)
                        if pattern_str in to_str(root_diag):
                            return True
                
                for i in range(1, board.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player2 == 2:
                            pattern_str = '{0}{0}{0}3'.format(self.player_number)
                        else:
                            pattern_str = '{0}{0}{0}4'.format(self.player_number)
                        if pattern_str in diag:
                            return True
                        if player2 == 2:
                            for i in pattern5:
                                pattern_str = i.format(player2)
                                if pattern_str in diag:
                                    return True
                        else:
                            for i in pattern6:
                                pattern_str = i.format(player2)
                                if pattern_str in diag:
                                    return True
        return False

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        if self.player_number == 1:
            player2 = 2
        else:
            player2 = 1
        # Some patterns for the calculating utility function
        pattern1 = ['{0}{0}{0}0' , '0{0}{0}{0}','{0}0{0}{0}','{0}{0}0{0}']
        pattern2 = ['{0}{0}{0}{0}']
        pattern5 = ['{0}{0}{0}1' , '1{0}{0}{0}','{0}1{0}{0}','{0}{0}1{0}']
        pattern6 = ['{0}{0}{0}2' , '2{0}{0}{0}','{0}2{0}{0}','{0}{0}2{0}']
        pattern7 = ['1{0}{0}{0}1']
        pattern8 = ['2{0}{0}{0}2']
        count = 0
        to_str = lambda a: ''.join(a.astype(str))
        # For checking in horizontal directions
        for row in board:
            for i in pattern1:
                pattern_str = i.format(self.player_number)
                if pattern_str in to_str(row):
                    count+=8
            for i in pattern2:
                pattern_str = i.format(self.player_number)
                if pattern_str in to_str(row):
                    count+=300
            if player2 == 2:
                for i in pattern5:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        count+=100
            else:
                for i in pattern6:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        count+=100
            if player2 == 2:
                for i in pattern7:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        count+=150
            else:
                for i in pattern8:
                    pattern_str = i.format(player2)
                    if pattern_str in to_str(row):
                        count+=150  

        # For checking in vertical directions
        for row in board.T:
            pattern_str = '0{0}{0}{0}'.format(self.player_number)
            if pattern_str in to_str(row):
                count+=8
            pattern_str = '00{0}{0}'.format(self.player_number)
            if pattern_str in to_str(row):   
                count+=4
            pattern_str = '{0}{0}{0}{0}'.format(self.player_number)
            if pattern_str in to_str(row):
                count+=10
            if player2 == 2:
                pattern_str = '1{0}{0}{0}'.format(player2)               
                if pattern_str in to_str(row):
                    count+=100
            else:
                pattern_str = '2{0}{0}{0}'.format(player2)
                if pattern_str in to_str(row):
                    count+=100
        
        # For checking in diagonals
        for op in [None, np.fliplr]:
                op_board = op(board) if op else board
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                pattern_str = '{0}{0}{0}{0}'.format(self.player_number)
                if pattern_str in to_str(root_diag):
                    count+=300
                if player2 == 2:
                    for i in pattern5:
                        pattern_str = i.format(player2)
                        if pattern_str in to_str(root_diag):
                            count+=150
                else:
                    for i in pattern6:
                        pattern_str = i.format(player2)
                        if pattern_str in to_str(root_diag):
                            count+=150
                for i in range(1, board.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        pattern_str = '{0}{0}{0}{0}'.format(self.player_number)
                        if pattern_str in diag:
                            count+=300
                        if player2 == 2:
                            for i in pattern5:
                                pattern_str = i.format(player2)
                                if pattern_str in diag:
                                    count+=150
                        else:
                            for i in pattern6:
                                pattern_str = i.format(player2)
                                if pattern_str in diag:
                                    count+=150
        return count  

    def update_board(self, move, player_num):
        if 0 in self.new_board[:,move]:
            update_row = -1
            for row in range(1, self.new_board.shape[0]):
                update_row = -1
                if self.new_board[row, move] > 0 and self.new_board[row-1, move] == 0:
                    update_row = row-1
                elif row==self.new_board.shape[0]-1 and self.new_board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    self.new_board[update_row, move] = player_num
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))
        # print(board[5])

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move