import time
board = [["-" for _ in range(3)] for _ in range(3)]
player = "X"

def print_board():
    print(" " + " ".join(f"{j:5}" for j in range(3)))
    for i, row in enumerate(board):
        print(f"{i:2} │ " + "│  ".join(f"{cell:3}" for cell in row))
        if i < len(board) - 1:  # Print separator except after the last row
            print("─ " * 10)

    
def is_valid_move(row, col):
    if row < 0 or row > 2 or col < 0 or col > 2:
        print("Invalid move.")
        return False
    if board[row][col] != "-":
        print("This spapce is already taken.")
        return False
    return True

def clear_board():
    global board
    board = [["-" for _ in range(3)] for _ in range(3)]


def minimax(player, depth, alpha, beta):
    if check_win("O"):
        return 10, None, None
    elif check_win("X"):
        return -10, None, None
    elif check_tie() or depth == 0:
        return 0, None, None
    
    optimal_row, optimal_col = None, None

    if player == "O":
        best = -float("inf")
        should_break = False
        for row in range(3):
            if should_break:
                break
            for col in range(3):
                if board[row][col] == "-":
                    place_player("O", row, col)
                    score, _, _ = minimax("X", depth - 1, alpha, beta)
                    place_player("-", row, col)
                    if score > best:
                        best = score
                        optimal_row, optimal_col = row, col
                    alpha = max(alpha, best)
                    if alpha >= beta:
                        should_break = True
                        break
        return best, optimal_row, optimal_col
    
    if player == "X":
        worst = float("inf")
        should_break = False
        for row in range(3):
            if should_break:
                break
            for col in range(3):
                if board[row][col] == "-":
                    place_player("X", row, col)
                    score, _, _ = minimax("O", depth - 1, alpha, beta)
                    place_player("-", row, col)
                    if score < worst:
                        worst = score
                        optimal_row, optimal_col = row, col
                    beta = min(beta, worst)
                    if beta <= alpha:
                        should_break = True
                        break
        return worst, optimal_row, optimal_col


def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): # Check row
            return True
        if all(board[j][i] == player for j in range(3)): # Check col
            return True

    # check diagonals
    if board[0][0] == player and board [1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board [1][1] == player and board[2][0] == player:
        return True
    return

def check_tie():
    return all(board[i][j] != "-" for i in range(3) for j in range(3))

def place_player(player, row, col):
    board[row][col] = player

def take_turn(player):
    if player == "X":
        while True:
            print(f"{player}'s Turn")
            try:
                row_input, col_input = map(int, input("Enter a position (row, col): ").split(','))
            except ValueError:
                print("Please enter valid integers")
                continue
            
            if is_valid_move(row_input, col_input):
                return row_input, col_input
            else:
                print("Invalid move.")
    else:
        print(f"{player}'s Turn")
        time.sleep(2)
        while True:
            worst, row_input, col_input = minimax(player, 4, -1000, 1000)
            if is_valid_move(row_input, col_input):
                return row_input, col_input

def main():
    global player
    while True:
        player = "X"
        clear_board()
        
        while True:
            print_board()  # Only print once per turn
            
            row_input, col_input = take_turn(player)
            place_player(player, row_input, col_input)

            if check_win(player):
                print_board()  # Show final board state
                print(f"{player} wins!")
                break

            if check_tie():
                print_board()  # Show final board state
                print("Tie")
                break

            player = "O" if player == "X" else "X"

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            print("Thanks for playing!")
            break



if __name__ == "__main__":
    main()