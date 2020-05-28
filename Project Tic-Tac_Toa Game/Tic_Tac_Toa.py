class TicTacToa:
    relative_position = [
        [1, 3], [2, 3], [3, 3],
        [1, 2], [2, 2], [3, 2],
        [1, 1], [2, 1], [3, 1]
    ]

    def __init__(self):
        self.board = list()
    
    def __str__(self):
        massage = ("-" * 9) + "\n" 
        for i in range(3):
            massage += "| {} {} {} |\n".format(self.board[i][0], self.board[i][1], self.board[i][2])
        massage += ("-" * 9) + "\n"
        return massage

    def print_game_board(self):
        print("-" * 9)
        for i in range(3):
            print("| {} {} {} |".format(self.board[i][0], self.board[i][1], self.board[i][2]))
        print("-" * 9)

    def make_board(self):
        for i in range(3):
            self.board.append(list(" " * 3))

    def get_real_coordinate(self,x, y):
        if len(x) > 1 or len(y) > 1:
            return "NAN"
        
        x, y = int(x), int(y)
        if x not in range(1,4) or y not in range(1, 4):
            return "boundaryError"

        idx = TicTacToa.relative_position.index([x, y])
        return [idx // 3, idx % 3]

    def check_win_status(self, player):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True
        return False

    def play_game(self):
        self.make_board()
        self.print_game_board()
        
        player_turn = 0
        empty_cell = 9

        while True:
            x, y = input("Enter the coordinates:").split()
            coordinate = self.get_real_coordinate(x, y)

            if coordinate == "NAN":
                print("You should enter numbers!")
                continue
            elif coordinate == "boundaryError":
                print("Coordinates should be from 1 to 3!")
                continue
            elif self.board[coordinate[0]][coordinate[1]] != " ":
                print("This cell is occupied! Choose another one!")
                continue
            
            player_sign = "X" if player_turn % 2 == 0 else "O"
            self.board[coordinate[0]][coordinate[1]] = player_sign
            empty_cell -= 1

            self.print_game_board()
            player_turn += 1

            if self.check_win_status(player_sign):
                print("{} wins".format(player_sign))
                break
            
            if empty_cell == 0:
                print("Draw")
                break

# Playing from here

tic_tac_toa = TicTacToa()
tic_tac_toa.play_game()

# print(tic_tac_toa)