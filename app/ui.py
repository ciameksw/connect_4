from game_logic import Board


def print_board(board: Board):
    for row in board:
        print("|", end="")
        for cell in row:
            print(cell, "|", end="", sep="")
        print("")
