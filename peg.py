'''
Robbie Decker
partner: Augustine Valdez
'''

from copy import deepcopy as copy
import argparse
from animation import draw

class Node():
    def __init__(self, board, jumpfrom = None, jumpover = None, jumpto = None):
        self.board = board
        self.jumpfrom = jumpfrom
        self.jumpover = jumpover
        self.jumpto = jumpto

class peg:
    def __init__(self, start_row, start_col, rule):
        self.size = 5
        self.start_row, self.start_col, self.rule = start_row, start_col, rule
        # board
        self.board = [[1 for j in range(i+1)] for i in range(self.size)]
        self.board[start_row][start_col] = 0
        self.start = Node(copy(self.board))
        # path
        self.path = []
        # Do some initialization work here if you need:



    def draw(self):
        if self.success():
            draw(self.path, self.start_row, self.start_col, self.rule)
        else:
            print("No solution were found!")

   
    def success(self):
        total = 0
        for i in self.board:
            for j in range(len(i)):
                total += i[j]

        if total == 1:
            return True
        else:
            return False
            

    def solve(self):
        rowDirection = [-1, 1, 0, 0, 1, -1]
        colDirection = [0, 0, -1, 1, 1, -1]
        jump_row = [-2, 2, 0, 0, 2, -2]
        jump_col = [0, 0, -2, 2, 2, -2]


        if self.success():
            return True

        for row in self.board:
            for y in range(len(row)):
                x = (len(row)-1)
                current = self.board[x][y]

                if current == 0:
                    for i in range(6):
                        jump_over_X = x + rowDirection[i]
                        jump_over_Y = y + colDirection[i]
                        # JUMP TO
                        if jump_over_X > -1 and jump_over_X < 5 and jump_over_Y in range(0, len(self.board[jump_over_X])) and jump_over_Y <= jump_over_X:
                            #if self.board[jump_over_X][jump_over_Y]: 
                                jump_over_value = self.board[jump_over_X][jump_over_Y]
                                jump_from_X = x + jump_row[i]
                                jump_from_Y = y + jump_col[i]
                                # JUMP OVER
                                if jump_from_X > -1 and jump_from_X < 5 and jump_from_Y in range(0, len(self.board[jump_from_X])) and jump_from_Y <= jump_from_X:
                                    if self.board[jump_from_X][jump_from_Y] == 1:
                                        jump_from_value = self.board[jump_from_X][jump_from_Y]
                                        jump_to_value = self.board[x][y]
                                        # checking to see if its jumping over peg, jumping from pegping to the empty spot 
                                        if jump_from_value == 1 and jump_to_value == 0 and jump_over_value == 1:
                                            self.board[jump_from_X][jump_from_Y] = 0
                                            self.board[jump_over_X][jump_over_Y] = 0
                                            self.board[x][y] = 1
                                            return_state = copy(self.board)
                                            newNode = Node(return_state, (jump_from_X, jump_from_Y), (jump_over_X, jump_over_Y), (x, y))
                                            self.path.append(newNode)
                                            if self.rule == 0:

                                                if self.solve():
                                                    return True
                                            
                                                self.path.remove(newNode)
                                                self.board[jump_from_X][jump_from_Y] = 1
                                                self.board[jump_over_X][jump_over_Y] = 1
                                                self.board[x][y] = 0
                                            elif self.rule == 1:
                                                beginning_node = self.path[0]
                                                beginning_r = self.start_row
                                                beginning_c = self.start_col
                                                ending_r, ending_c = newNode.jumpfrom
                                                print("c",beginning_c)
                                                print("r",beginning_r)
                                                if (beginning_r == ending_r) and (beginning_c == ending_c) and self.solve():
                                                    return True
                                                self.path.remove(newNode)
                                                self.board[jump_from_X][jump_from_Y] = 1
                                                self.board[jump_over_X][jump_over_Y] = 1
                                                self.board[x][y] = 0

        return False



        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='peg game')

    parser.add_argument('-hole', dest='position', required = True, nargs = '+', type = int, help='initial position of the hole')
    parser.add_argument('-rule', dest='rule', required = True, type = int, help='index of rule')

    args = parser.parse_args()

    start_row, start_col = args.position
    if start_row > 4:
        print("row must be less or equal than 4")
        exit()
    if start_col > start_row:
        print("column must be less or equal than row")
        exit()

    # Example: 
    # python peg.py -hole 0 0 -rule 0
    game = peg(start_row, start_col, args.rule)
    game.solve()
    game.draw()
    