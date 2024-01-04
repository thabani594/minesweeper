import random 
import re


class Board:
    def __init__(self,dim_size,num_of_bombs):
        self.dim_size = dim_size
        self.num_of_bombs = num_of_bombs


        self.board = self.make_new_board()
        self.assign_values_board()

        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)]for _ in range(self.dim_size)]
        bombs_planted = 0
        
        while bombs_planted < self.num_of_bombs:
            loc = random.randint(0,self.dim_size**2 -1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                continue
            board[row][col] = "*"
            bombs_planted += 1

        return board 

    def assign_values_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r,c)

    def get_num_neighbouring_bombs(self,row,col):

        num_neighbouring_bombs = 0
        for r in range(max(0,row-1),min(self.dim_size - 1,row + 1)+1):
            for c in range(max(0,col-1),min(self.dim_size - 1,col+1)+1):
                if r == row and c == col :
                    continue
                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1
                return num_neighbouring_bombs


    def dig(self,row,col):
        self.dug.add((row,col))
        if self.board[row][col] =="*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0,row-1),min(self.dim_size - 1,row + 1)+1):
            for c in range(max(0,col-1),min(self.dim_size - 1,col-1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True
    
    def __str__(self):
        visible_board = [[None for _ in range (self.dim_size)]for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if(row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = "  "
        result = " "
        for row in visible_board:
            result += " ".join(row) + "\n"
            return result
        

def play(dim_size = 10,num_of_bombs = 10):
    board = Board(dim_size,num_of_bombs)

    safe = True

    while len(board.dug) < board.dim_size**2 - num_of_bombs:
        print(num_of_bombs)
        user_input =re.split(',(\\s)*',input("Where would you like to dig?input as row,col:  "))

        row,col = int(user_input[0]),int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location.Try again.")
            continue
        safe = board.dig(row,col)
        if not safe:
            break

    if safe:
        print("You won.")
    else:
        print("Sorry game over.")
        board.dug = [(r,c)for r in range(board.dim_size)for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()


