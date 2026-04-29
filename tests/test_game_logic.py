import pytest

from app.config import Config
from app.game_logic import GameLogic, MakeMoveResult


@pytest.fixture
def config():
    cfg = Config()
    cfg.reset()
    yield cfg
    cfg.reset()


@pytest.fixture
def game_logic(config):
    return GameLogic(config)


def test_create_board_returns_empty_board(game_logic):
    board = game_logic.create_board()

    assert len(board) == game_logic.config.rows
    assert all(len(row) == game_logic.config.columns for row in board)
    assert all(cell == game_logic.config.empty for row in board for cell in row)


def test_available_moves_returns_all_columns_for_empty_board(game_logic):
    board = game_logic.create_board()

    assert game_logic.available_moves(board) == list(range(game_logic.config.columns))


def test_make_move_places_piece_in_lowest_available_row(game_logic):
    board = game_logic.create_board()

    result = game_logic.make_move(board, 0, game_logic.config.player1)

    assert result.row == game_logic.config.rows - 1
    assert result.column == 0
    assert result.board[result.row][result.column] == game_logic.config.player1


def test_make_move_raises_for_invalid_column(game_logic):
    board = game_logic.create_board()

    with pytest.raises(ValueError, match="Invalid column: -1"):
        game_logic.make_move(board, -1, game_logic.config.player1)


def test_make_move_raises_for_full_column(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
    ]

    with pytest.raises(ValueError, match="Column 0 is full"):
        game_logic.make_move(board, 0, game_logic.config.player2)


def test_winner_detects_horizontal_line(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, p1, p1, p1, e, e, e],
    ]

    result = MakeMoveResult(board, 5, 3)

    assert game_logic.winner(result) == game_logic.config.player1


def test_winner_detects_vertical_line(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
    ]

    result = MakeMoveResult(board, 2, 0)

    assert game_logic.winner(result) == game_logic.config.player1


def test_winner_detects_diagonal_down_right(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [e, p1, e, e, e, e, e],
        [e, e, p1, e, e, e, e],
        [e, e, e, p1, e, e, e],
    ]

    result = MakeMoveResult(board, 5, 3)

    assert game_logic.winner(result) == game_logic.config.player1


def test_winner_detects_diagonal_up_right(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, p1, e, e, e],
        [e, e, p1, e, e, e, e],
        [e, p1, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
    ]

    result = MakeMoveResult(board, 0, 3)

    assert game_logic.winner(result) == game_logic.config.player1


def test_winner_returns_none_for_empty_board(game_logic):
    board = game_logic.create_board()

    result = MakeMoveResult(board, 0, 0)

    assert game_logic.winner(result) is None


def test_winner_returns_none_for_no_win(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, p1, p1, e, e, e, e],
    ]

    result = MakeMoveResult(board, 5, 2)

    assert game_logic.winner(result) is None


def test_winner_respects_win_length_5(game_logic):
    game_logic.config.update(win_length=5)

    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, p1, p1, p1, p1, e, e],
    ]

    result = MakeMoveResult(board, 5, 4)

    assert game_logic.winner(result) == game_logic.config.player1


def test_board_is_full_detects_full_board(game_logic):
    p1 = game_logic.config.player1
    board = [
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
    ]

    assert game_logic.board_is_full(board) is True


def test_board_is_full_detects_non_full_board(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, e, e, e, e, e, e],
    ]

    assert game_logic.board_is_full(board) is False


def test_next_player_returns_player1_when_counts_are_equal(game_logic):
    board = game_logic.create_board()

    assert game_logic.next_player(board) == game_logic.config.player1


def test_next_player_returns_player2_when_player1_has_more_pieces(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    p2 = game_logic.config.player2
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, p1, e, e, e, e, e],
        [p1, p2, e, e, e, e, e],
    ]

    assert game_logic.next_player(board) == game_logic.config.player2


def test_is_final_returns_true_for_win(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, p1, p1, p1, e, e, e],
    ]

    result = MakeMoveResult(board, 5, 3)

    assert game_logic.is_final(result) is True


def test_is_final_returns_true_for_full_board(game_logic):
    p1 = game_logic.config.player1
    board = [
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
        [p1, p1, p1, p1, p1, p1, p1],
    ]
    result = MakeMoveResult(board, 0, 0)

    assert game_logic.is_final(result) is True


def test_count_pieces_empty_board(game_logic):
    board = game_logic.create_board()

    assert game_logic.count_pieces(board) == 0


def test_count_pieces_mixed(game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    p2 = game_logic.config.player2
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, p1, e, e, e, e, e],
        [p1, p2, e, e, e, e, e],
    ]

    assert game_logic.count_pieces(board) == 3
