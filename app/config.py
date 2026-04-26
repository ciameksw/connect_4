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

        # AI settings
        self.minimax_depth = 4

        self.exact_win_length_score = 100
        self.one_missing_to_win_score = 5
        self.two_missing_to_win_score = 2
        self.opponent_threat_penalty = -4

        self.terminal_win_score = 1000
        self.terminal_loss_score = -1000

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
