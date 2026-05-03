class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_defaults()
        return cls._instance

    def _set_defaults(self):
        # Game rules
        self.rows = 6
        self.columns = 7
        self.win_length = 4

        # Board states
        self.empty = 0
        self.player1 = 1
        self.player2 = 2

        # Minimax search depth
        self.minimax_search_depth = 6

        # Heuristic points for our potential windows
        self.heuristic_score_exact_win_length = 80
        self.heuristic_score_one_missing = 9
        self.heuristic_score_two_missing = 3
        self.heuristic_score_three_missing = 0.5

        # Heuristic penalties for opponent threats
        self.heuristic_penalty_opponent_one_missing = -40
        self.heuristic_penalty_opponent_two_missing = -2.0
        self.heuristic_penalty_opponent_three_missing = -0.5

        # Positional/depth modifiers for heuristic value
        self.heuristic_score_center_column = 3
        self.heuristic_score_multiplier = 1.5
        self.heuristic_depth_discount_ratio = 0.25

        # Terminal board scores
        self.terminal_score_win = 80
        self.terminal_score_loss = -80

    def reset(self):
        """Reset all settings to their default values."""
        self._set_defaults()

    def update(self, **kwargs):
        """Update settings with provided keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Config has no attribute '{key}'")

    def to_dict(self):
        """Return a dictionary representation of the current configuration."""
        return {key: getattr(self, key) for key in self.__dict__ if not key.startswith("_")}
