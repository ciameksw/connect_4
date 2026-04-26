import pytest

from app.config import Config


@pytest.fixture
def config():
    cfg = Config()  # Create config
    cfg.reset()  # Reset to defaults before each test
    yield cfg  # Provide config for the tests
    cfg.reset()  # Reset to defaults after each test


def test_config_is_singleton():
    assert Config() is Config()


def test_default_values_are_loaded(config):
    assert config.rows == 6
    assert config.columns == 7
    assert config.win_length == 4
    assert config.empty == 0
    assert config.player1 == 1
    assert config.player2 == 2
    assert config.minimax_search_depth == 4
    assert config.heuristic_score_exact_win_length == 80
    assert config.heuristic_score_one_missing == 9
    assert config.heuristic_score_two_missing == 3
    assert config.heuristic_score_three_missing == 0.5
    assert config.heuristic_penalty_opponent_one_missing == -40
    assert config.heuristic_penalty_opponent_two_missing == -2.0
    assert config.heuristic_penalty_opponent_three_missing == -0.5
    assert config.heuristic_score_center_column == 3
    assert config.heuristic_score_multiplier == 1.5
    assert config.heuristic_depth_discount_ratio == 0.25
    assert config.terminal_score_win == 80
    assert config.terminal_score_loss == -80


def test_update_changes_existing_values(config):
    config.update(rows=8, win_length=5, minimax_search_depth=6)

    assert config.rows == 8
    assert config.win_length == 5
    assert config.minimax_search_depth == 6


def test_update_unknown_key_raises(config):
    with pytest.raises(AttributeError, match="Config has no attribute 'does_not_exist'"):
        config.update(does_not_exist=123)


def test_reset_restores_defaults(config):
    config.update(rows=10, win_length=5, minimax_search_depth=7)
    config.reset()

    assert config.rows == 6
    assert config.win_length == 4
    assert config.minimax_search_depth == 4


def test_to_dict_returns_public_settings_only(config):
    data = config.to_dict()

    assert "_instance" not in data
    assert data["rows"] == 6
    assert data["columns"] == 7
    assert data["win_length"] == 4
