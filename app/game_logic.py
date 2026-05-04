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
        """Initialize GameLogic with configuration and direction axes."""
        self.config = config or Config()
        self._axes = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def create_board(self) -> Board:
        """Create a new empty game board."""
        return [
            [self.config.empty for _ in range(self.config.columns)] for _ in range(self.config.rows)
        ]

    def available_moves(self, board: Board) -> list[int]:
        """Return a list of columns where a move can be made (not full)."""
        return [i for i, cell in enumerate(board[0]) if cell == self.config.empty]

    def winner(self, make_move_result: MakeMoveResult) -> Optional[int]:
        """Check if the last move resulted in a win."""
        board = make_move_result.board
        row = make_move_result.row
        column = make_move_result.column
        player = board[row][column]

        if player == self.config.empty:
            return None

        # Check all four directions (horizontal, vertical, diagonal down-right, diagonal down-left)
        for delta_row, delta_column in self._axes:
            connected = 1

            # For every direction, we count both ways (positive and negative)
            connected += self._count_consecutive_in_dir(
                board, row, column, delta_row, delta_column, player
            )
            connected += self._count_consecutive_in_dir(
                board, row, column, -delta_row, -delta_column, player
            )

            if connected >= self.config.win_length:
                return player

        return None

    def is_final(self, make_move_result: MakeMoveResult) -> bool:
        """Check if the game is over (win or draw)."""
        return self.winner(make_move_result) is not None or self.board_is_full(
            make_move_result.board
        )

    def board_is_full(self, board: Board) -> bool:
        """Check if the board is completely filled (no empty cells)."""
        for row in board:
            for cell in row:
                if cell == self.config.empty:
                    return False
        return True

    def next_player(self, board: Board) -> int:
        """Determine which player's turn is next based on the board state."""
        player1_count = 0
        player2_count = 0

        for row in board:
            for cell in row:
                if cell == self.config.player1:
                    player1_count += 1
                elif cell == self.config.player2:
                    player2_count += 1

        # Player 1 always starts, so if counts are equal, it's player 1's turn
        return self.config.player1 if player1_count == player2_count else self.config.player2

    def make_move(self, board: Board, move: int, player: int) -> MakeMoveResult:
        """Place a piece for the player in the specified column and return the new board state."""
        if not (0 <= move < self.config.columns):
            raise ValueError(f"Invalid column: {move}")

        new_board = self._deep_board_copy(board)

        # For 6 rows, go from 5 to 0
        for row_idx in range(self.config.rows - 1, -1, -1):
            if new_board[row_idx][move] == self.config.empty:
                new_board[row_idx][move] = player
                return MakeMoveResult(new_board, row_idx, move)

        raise ValueError(f"Column {move} is full")

    def _deep_board_copy(self, board: Board) -> Board:
        """Return a deep copy of the board (new list of lists)."""
        return [row.copy() for row in board]

    def _count_consecutive_in_dir(
        self, board: Board, row: int, col: int, delta_row: int, delta_column: int, player: int
    ) -> int:
        """Count consecutive pieces for a player in a given direction from a starting cell."""
        count = 0

        # Start from the next cell in the given direction
        r = row + delta_row
        c = col + delta_column

        # Keep counting while we're within bounds and the cell belongs to the same player
        while 0 <= r < self.config.rows and 0 <= c < self.config.columns and board[r][c] == player:
            count += 1

            # Move to the next cell in the same direction
            r += delta_row
            c += delta_column

        return count

    def count_pieces(self, board: Board) -> int:
        """Count the total number of pieces on the board (non-empty cells)."""
        total_pieces = 0
        for row in board:
            for cell in row:
                if cell != self.config.empty:
                    total_pieces += 1
        return total_pieces
