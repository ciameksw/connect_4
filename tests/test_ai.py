import pytest

from app.ai import AI
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


@pytest.fixture
def ai(game_logic):
    return AI(game_logic)


def test_choose_best_move_prefers_center_column_on_empty_board(ai, game_logic):
    board = game_logic.create_board()
    result = MakeMoveResult(board, 0, 0)

    assert ai.choose_best_move(result) == game_logic.config.columns // 2


def test_choose_best_move_takes_immediate_winning_move(ai, game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    p2 = game_logic.config.player2
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p2, p2, p2, e, e, e, e],
        [p1, p1, p1, e, e, e, e],
    ]
    result = MakeMoveResult(board, 5, 2)

    assert ai.choose_best_move(result) == 3


def test_choose_best_move_blocks_immediate_opponent_win(ai, game_logic):
    e = game_logic.config.empty
    p1 = game_logic.config.player1
    p2 = game_logic.config.player2
    board = [
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [e, e, e, e, e, e, e],
        [p1, p1, p1, e, e, e, e],
        [p2, p2, p2, e, e, e, e],
    ]
    result = MakeMoveResult(board, 5, 2)

    assert ai.choose_best_move(result) == 3


def test_choose_best_move_raises_error_when_no_valid_moves(ai, game_logic):
    with pytest.raises(ValueError, match="No valid moves available to choose from"):
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
        assert ai.choose_best_move(result) == 3
