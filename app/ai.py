from dataclasses import dataclass
from math import inf
from typing import Optional

from app.config import Config
from app.game_logic import Board, GameLogic, MakeMoveResult


@dataclass
class MinimaxResult:
    score: float
    move: Optional[int]


class AI:
    def __init__(self, game_logic: GameLogic | None = None, config: Config | None = None):
        self.game_logic = game_logic or GameLogic(config)
        self.config = self.game_logic.config

    def choose_best_move(self, make_move_result: MakeMoveResult) -> int:
        # Select next player based on the board state
        player = self.game_logic.next_player(make_move_result.board)

        # Run minimax to find the best move for the current player
        result = self._minimax(make_move_result, player, self.config.minimax_search_depth)

        if result.move is None:
            raise ValueError("No valid moves available to choose from")
        return result.move

    def _minimax(
        self,
        make_move_result: MakeMoveResult,
        player: int,
        depth: int,
        alpha: float = -inf,
        beta: float = inf,
    ) -> MinimaxResult:
        # Check for terminal state or depth limit
        if self.game_logic.is_final(make_move_result):
            return MinimaxResult(score=self._terminal_score(make_move_result), move=None)

        if depth == 0:
            return MinimaxResult(
                score=self._evaluate_heuristic_score(
                    make_move_result, self.config.minimax_search_depth - depth
                ),
                move=None,
            )

        best_move = None

        # Maximize score for player1, minimize score for player2
        if player == self.config.player1:
            best_score = -inf
            for move in self.game_logic.available_moves(make_move_result.board):
                child = self.game_logic.make_move(make_move_result.board, move, player)
                result = self._minimax(
                    child,
                    self.config.player2,
                    depth - 1,
                    alpha,
                    beta,
                )

                if result.score > best_score:
                    best_score = result.score
                    best_move = move

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        else:
            best_score = inf
            for move in self.game_logic.available_moves(make_move_result.board):
                child = self.game_logic.make_move(make_move_result.board, move, player)
                result = self._minimax(
                    child,
                    self.config.player1,
                    depth - 1,
                    alpha,
                    beta,
                )

                if result.score < best_score:
                    best_score = result.score
                    best_move = move

                beta = min(beta, best_score)
                if alpha >= beta:
                    break

        return MinimaxResult(score=float(best_score), move=best_move)

    def _terminal_score(self, make_move_result: MakeMoveResult) -> float:
        # A terminal score is calculated only when the board is in a final state.
        # We check if it's a win for player1, a win for player2, or a draw.
        w = self.game_logic.winner(make_move_result)
        if w == self.config.player1:
            return float(self.config.terminal_score_win)
        if w == self.config.player2:
            return float(self.config.terminal_score_loss)
        return 0.0

    def _evaluate_heuristic_score(
        self, make_move_result: MakeMoveResult, depth_from_root: int
    ) -> float:
        board = make_move_result.board
        score = 0.0

        # Center column gives more opportunities to connect 4,
        # so we give it a bonus in the heuristic score.
        score += self._evaluate_center_column(board)

        # We evaluate all possible windows of length win_length
        # in all directions and sum up their scores.
        # Horizontal
        score += self._evaluate_windows_in_direction(board, 0, 1)
        # Vertical
        score += self._evaluate_windows_in_direction(board, 1, 0)
        # Diagonal down-right
        score += self._evaluate_windows_in_direction(board, 1, 1)
        # Diagonal up-right
        score += self._evaluate_windows_in_direction(board, 1, -1)

        # Normalize the score to prevent it from becoming too large with more pieces on the board.
        score = self._normalize_score(board, score)

        # Multiply the score by a heuristic multiplier to adjust
        # the importance of the heuristic evaluation relative to terminal states.
        score *= self.config.heuristic_score_multiplier

        # Apply a discount to the score based on how deep we are in the search tree.
        return self._discount_score(score, depth_from_root)

    def _evaluate_window(self, window: list[int]) -> float:
        player1 = self.config.player1
        player2 = self.config.player2
        window_length = self.config.win_length

        player1_count = window.count(player1)
        player2_count = window.count(player2)

        # Only evaluate windows when they contain pieces from one player and empty spaces,
        # because mixed windows are not useful for either player.

        if player2_count == 0:
            if player1_count == window_length:
                return float(self.config.heuristic_score_exact_win_length)
            if player1_count == window_length - 1:
                return float(self.config.heuristic_score_one_missing)
            if player1_count == window_length - 2:
                return float(self.config.heuristic_score_two_missing)
            if player1_count == window_length - 3:
                return float(self.config.heuristic_score_three_missing)

        if player1_count == 0:
            if player2_count == window_length - 1:
                return float(self.config.heuristic_penalty_opponent_one_missing)
            if player2_count == window_length - 2:
                return float(self.config.heuristic_penalty_opponent_two_missing)
            if player2_count == window_length - 3:
                return float(self.config.heuristic_penalty_opponent_three_missing)

        return 0.0

    def _evaluate_center_column(self, board: Board) -> float:
        center_column = self.config.columns // 2
        score = 0.0
        for row in board:
            if row[center_column] == self.config.player1:
                score += self.config.heuristic_score_center_column
            elif row[center_column] == self.config.player2:
                score -= self.config.heuristic_score_center_column
        return score

    def _evaluate_windows_in_direction(self, board: Board, delta_row: int, delta_col: int) -> float:
        rows = self.config.rows
        cols = self.config.columns
        win_length = self.config.win_length
        score = 0.0

        # Iterate over every possible starting cell on the board
        for row in range(rows):
            for col in range(cols):
                window = []
                # Build a window of length win_length in the given direction
                for i in range(win_length):
                    r = row + delta_row * i  # Calculate row index for this step
                    c = col + delta_col * i  # Calculate column index for this step
                    # Check if the calculated cell is within the board boundaries
                    if 0 <= r < rows and 0 <= c < cols:
                        window.append(board[r][c])
                    else:
                        break  # If out of bounds, stop building this window
                # If the window is the correct length, evaluate it and add to the score
                if len(window) == win_length:
                    score += self._evaluate_window(window)
        return score

    def _normalize_score(self, board: Board, score: float) -> float:
        # Divide the score by the total number of pieces on the board
        # to prevent it from growing too large as the game progresses.
        total_pieces = self.game_logic.count_pieces(board)
        if total_pieces == 0:
            return score
        return score / total_pieces

    def _discount_score(self, score: float, depth_from_root: int) -> float:
        # By discounting the score based on depth,
        # we encourage the AI to find winning moves sooner and losing moves later in the search tree.
        depth_fraction = depth_from_root / self.config.minimax_search_depth
        discount_factor = 1 - self.config.heuristic_depth_discount_ratio * depth_fraction
        return score * discount_factor
