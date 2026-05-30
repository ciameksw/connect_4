import pygame
from pygame.event import Event

from app.ai import AI
from app.config import Config
from app.game_logic import GameLogic
from app.ui.game_view import GameView
from app.ui.menu_view import MenuView
from app.ui.options_view import OptionsView


class Connect4Game:
    def __init__(self):
        """Initialize the game, set up logic, views, and display."""
        # Initialize Pygame
        pygame.init()

        # Setup game logic classes
        self.config = Config()
        self.game_logic = GameLogic(self.config)
        self.ai = AI(self.game_logic, self.config)

        # Setup display parameters
        self.cell_size = 80
        self.width = self.config.columns * self.cell_size
        self.height = (self.config.rows + 2) * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Set window title
        pygame.display.set_caption("Connect 4")

        # Setup pygame/view classes
        self.menu_view = MenuView(self.screen)
        self.options_view = OptionsView(self.screen, self.config)
        self.game_view = GameView(
            self.screen,
            self.width,
            self.height,
            self.cell_size,
            self.config,
            self.game_logic,
        )

        # Start in menu view
        self.current_view = self.menu_view.id

        # Store who the player is (default to player 1, but can be changed in menu)
        self.player = self.config.player1

    def apply_config_changes(self) -> None:
        """Apply changes from the config, updating window size, logic, and views."""
        # Change window size based on new config
        self.width = self.config.columns * self.cell_size
        self.height = (self.config.rows + 2) * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Update GameLogic and AI
        self.game_logic = GameLogic(self.config)
        self.ai = AI(self.game_logic, self.config)

        # Update the views
        self.game_view = GameView(
            self.screen,
            self.width,
            self.height,
            self.cell_size,
            self.config,
            self.game_logic,
        )
        self.options_view = OptionsView(self.screen, self.config)
        self.menu_view = MenuView(self.screen)

    def run(self):
        """Main loop dispatcher: runs the appropriate view loop based on current view."""
        # Main game loop that runs the appropriate view loop based on the current view
        while True:
            if self.current_view == self.menu_view.id:
                self.screen = pygame.display.set_mode((800, 600))
                self.game_view.screen = self.screen
                self.run_menu_loop()
            elif self.current_view == self.options_view.id:
                self.screen = pygame.display.set_mode((800, 600))
                self.game_view.screen = self.screen
                self.run_options_loop()
            elif self.current_view == self.game_view.id:
                self.screen = pygame.display.set_mode((self.width, self.height))
                self.game_view.screen = self.screen
                self.run_game_loop()

    def run_menu_loop(self) -> None:
        """Run the event loop for the main menu view."""
        self.menu_view.show()
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                # Check for quit events
                self.check_and_handle_quit(event)

                # Get the click result from the menu view
                result = self.menu_view.handle_button_event(event)

                # Update the current view based on the click result
                if result == self.menu_view.start_as_1_id:
                    self.player = self.config.player1
                    self.game_view.reset_game(self.player)
                    self.current_view = self.game_view.id
                    in_menu = False
                elif result == self.menu_view.start_as_2_id:
                    self.player = self.config.player2
                    self.game_view.reset_game(self.player)
                    self.current_view = self.game_view.id
                    in_menu = False
                elif result == self.menu_view.options_id:
                    self.current_view = self.options_view.id
                    in_menu = False

    def run_options_loop(self) -> None:
        """Run the event loop for the options view, handling config editing."""
        self.options_view.show()
        in_options = True
        while in_options:
            for event in pygame.event.get():
                # Check for quit events
                self.check_and_handle_quit(event)

                # Handle button events for options view
                self.options_view.handle_button_event(event)

                # Handle editing options
                if event.type == pygame.KEYDOWN:
                    if not self.options_view.edit_mode:
                        self.options_view.handle_event_in_select_mode(event)
                    else:
                        self.options_view.handle_event_in_edit_mode(event)

                # Check for ESC to go back to menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # First apply the config
                    self.apply_config_changes()
                    self.current_view = self.menu_view.id
                    in_options = False

                self.options_view.show()

    def run_game_loop(self) -> None:
        """Run the event loop for the game view, handling moves and animations."""
        self.game_view.show()

        # If player 2 starts, make the first move for the AI
        if self.player == self.config.player2:
            ai_move = self.ai.choose_best_move(self.game_view.last_move)
            self.game_view.handle_move(ai_move)

        in_game = True
        while in_game:
            for event in pygame.event.get():
                # Check for quit events
                self.check_and_handle_quit(event)

                # Handle mouse movement for hover effect
                if event.type == pygame.MOUSEMOTION and not self.game_view.finished:
                    col = self.game_view.get_column_from_mouse(event.pos)
                    # Only draw hover token if it's a valid move
                    if col is not None and col in self.game_logic.available_moves(
                        self.game_view.board
                    ):
                        self.game_view.draw_hover_token(col)
                    # If it is not, clear the hover_col and clear the row above the board
                    else:
                        self.game_view.hover_col = None
                        self.game_view.fill_row_above_board()

                # Handle mouse click for making a move
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_view.finished:
                    col = self.game_view.get_column_from_mouse(event.pos)
                    # Only allow placing a token if it's a valid move for the current board state
                    if col is not None and col in self.game_logic.available_moves(
                        self.game_view.board
                    ):
                        # Make the player's move
                        self.game_view.handle_move(col)

                        # If the game is not finished after the player's move, make the AI move
                        if (
                            self.game_view.current_player != self.player
                            and not self.game_view.finished
                        ):
                            col = self.ai.choose_best_move(self.game_view.last_move)
                            self.game_view.handle_move(col)

                    # Clear the hover_col so the token hovers if the mouse is still over the column after the move
                    self.game_view.hover_col = None

                    # Prevent placing tokens when the animation is running
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)

                # Check for ESC to go back to menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_view = self.menu_view.id
                    in_game = False

    def check_and_handle_quit(self, event: Event) -> None:
        """Check for quit event and exit the game if triggered."""
        if event.type == pygame.QUIT:
            pygame.quit()
            return
