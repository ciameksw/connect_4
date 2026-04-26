from dataclasses import dataclass
from typing import Optional

from app.config import Config

Board = list[list[int]]


@dataclass
class MakeMoveResult:
    board: Board
    row: int
    column: int


class GameLogic:
    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.axes = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def create_board(self) -> Board:
        return [
            [self.config.empty for _ in range(self.config.columns)] for _ in range(self.config.rows)
        ]

    def deep_board_copy(self, board: Board) -> Board:
        return [row.copy() for row in board]

    def available_moves(self, board: Board) -> list[int]:
        return [i for i, cell in enumerate(board[0]) if cell == self.config.empty]

    def winner(self, make_move_result: MakeMoveResult) -> Optional[int]:
        board = make_move_result.board
        row = make_move_result.row
        column = make_move_result.column
        player = board[row][column]

        if player == self.config.empty:
            return None

        for delta_row, delta_column in self.axes:
            connected = 1
            connected += self._count_consecutive_in_dir(
                board, row, column, delta_row, delta_column, player
            )
            connected += self._count_consecutive_in_dir(
                board, row, column, -delta_row, -delta_column, player
            )

            if connected >= self.config.win_length:
                return player

        return None

    def _count_consecutive_in_dir(
        self, board: Board, row: int, col: int, delta_row: int, delta_column: int, player: int
    ) -> int:
        count = 0
        r = row + delta_row
        c = col + delta_column

        while 0 <= r < self.config.rows and 0 <= c < self.config.columns and board[r][c] == player:
            count += 1
            r += delta_row
            c += delta_column

        return count

    def is_final(self, make_move_result: MakeMoveResult) -> bool:
        return self.winner(make_move_result) is not None or self.board_is_full(
            make_move_result.board
        )

    def board_is_full(self, board: Board) -> bool:
        for row in board:
            for cell in row:
                if cell == self.config.empty:
                    return False
        return True

    def next_player(self, board: Board) -> int:
        player1_count = 0
        player2_count = 0

        for row in board:
            for cell in row:
                if cell == self.config.player1:
                    player1_count += 1
                elif cell == self.config.player2:
                    player2_count += 1
        return self.config.player1 if player1_count == player2_count else self.config.player2

    def make_move(self, board: Board, move: int, player: int) -> MakeMoveResult:
        if not (0 <= move < self.config.columns):
            raise ValueError(f"Invalid column: {move}")

        new_board = self.deep_board_copy(board)

        for row_idx in range(self.config.rows - 1, -1, -1):
            if new_board[row_idx][move] == self.config.empty:
                new_board[row_idx][move] = player
                return MakeMoveResult(new_board, row_idx, move)

        raise ValueError(f"Column {move} is full")
