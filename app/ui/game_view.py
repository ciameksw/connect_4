from typing import Optional

import pygame

from app.config import Config
from app.game_logic import GameLogic


class GameView:
    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        cell_size: int,
        config: Config,
        game_logic: GameLogic,
    ):
        """Initialize the game view with screen, dimensions, configuration, and game logic."""
        self.screen = screen
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.config = config
        self.game_logic = game_logic
        self.id = "game"

        # By default the player is player 1, but this can be changed in the menu
        self.player = self.config.player1

        # Store hovered column to prevent flickering
        self.hover_col: Optional[int] = None

        # UI
        self.message_font = pygame.font.SysFont("Arial", 32)
        self.esc_font = pygame.font.SysFont("Arial", 24)

        self.bg_color = (25, 55, 110)
        self.board_color = (40, 90, 200)
        self.player1_color = (220, 50, 50)
        self.player2_color = (240, 200, 40)
        self.text_color = (255, 255, 255)

    def reset_game(self, player: int) -> None:
        """Reset the game state for a new game, setting the starting player and board."""
        self.player = player

        # Create a new board
        self.board = self.game_logic.create_board()

        # Set game state variables
        self.current_player = self.config.player1
        self.finished = False
        self.last_move = None

    def show_message(self, message: str) -> None:
        """Display a message overlay above the board."""
        overlay = pygame.Surface((self.width, self.cell_size))
        overlay.fill(self.bg_color)

        # Add text
        text = self.message_font.render(message, True, self.text_color)
        text_rect = text.get_rect(center=(self.width // 2, self.cell_size // 2))
        overlay.blit(text, text_rect)

        # Display the overlay on the screen
        self.screen.blit(overlay, (0, self.cell_size))

        # Update the display to show the message
        pygame.display.update()

    def get_column_from_mouse(self, pos: tuple[int, int]) -> Optional[int]:
        """Return the column index corresponding to the mouse x position, or None if out of bounds."""
        x, _ = pos

        # Convert x coordinate to column index
        col = x // self.cell_size

        # Check if the column index is within bounds
        if 0 <= col < self.config.columns:
            return col
        return None

    def draw_hover_token(self, col: int) -> None:
        """Draw a preview token above the board in the hovered column."""
        # Redraw only if the hover column has changed
        if self.hover_col == col:
            return
        self.hover_col = col

        # Fill the top background, where animation of the falling token can be shown
        self.fill_row_above_board()

        # Select color based on current player
        color = (
            self.player1_color if self.current_player == self.config.player1 else self.player2_color
        )

        # Calculate coordinates and radius for the hover token
        x = col * self.cell_size + self.cell_size // 2
        y = self.cell_size // 2 + self.cell_size
        circle_radius = self.cell_size // 2 - 5

        # Draw the hover token
        pygame.draw.circle(self.screen, color, (x, y), circle_radius)
        pygame.display.update(
            (col * self.cell_size, self.cell_size, self.cell_size, self.cell_size)
        )

    def draw_board(self) -> None:
        """Draw the game board and all tokens on the screen."""
        # Fill the background
        board_background = pygame.Surface((self.width, self.cell_size * self.config.rows))
        board_background.fill(self.board_color)
        self.screen.blit(board_background, (0, 2 * self.cell_size))

        # Fill the top background, where animation of the falling token can be shown
        self.fill_row_above_board()

        # For each cell
        for r in range(self.config.rows):
            for c in range(self.config.columns):
                # Get the coordinates of the left, top corner of the cell
                x = c * self.cell_size
                y = (r + 2) * self.cell_size

                # Determine the color based on the cell value
                color = self.bg_color
                if self.board[r][c] == self.config.player1:
                    color = self.player1_color
                elif self.board[r][c] == self.config.player2:
                    color = self.player2_color

                # Draw a circle in the cell with the determined color
                circle_center = (x + self.cell_size // 2, y + self.cell_size // 2)
                circle_radius = self.cell_size // 2 - 5
                pygame.draw.circle(self.screen, color, circle_center, circle_radius)

        # Update the display to show the new board
        pygame.display.update()

    def show(self) -> None:
        """Render the game view, including the board and ESC message."""
        # Fill the background
        self.screen.fill(self.bg_color)

        # Show message to press ESC to go back to menu
        esc = self.esc_font.render("ESC - Go Back", True, self.text_color)
        esc_rect = esc.get_rect(center=(80, 25))
        self.screen.blit(esc, esc_rect)

        self.draw_board()

        pygame.display.update()

    def handle_move(self, col: int) -> None:
        """Handle a player's move, animate the token drop, update state, and check for game end."""
        move_result = self.game_logic.make_move(self.board, col, self.current_player)
        target_row = move_result.row

        # Animate the falling token
        self.animate_token_drop(col, target_row, self.current_player)

        # Make the move for provided column (update board state)
        self.board = move_result.board
        self.last_move = move_result

        # Redraw the board with the new move
        self.draw_board()

        # Check for winner or tie
        winner = self.game_logic.winner(move_result)
        if winner or self.game_logic.board_is_full(self.board):
            self.handle_game_end(winner)
            return

        # Switch to the next player
        self.current_player = self.game_logic.next_player(self.board)

    def animate_token_drop(self, col: int, target_row: int, player: int) -> None:
        """Animate the falling token effect for a move in the given column and row."""
        # Choose color based on the player
        color = self.player1_color if player == self.config.player1 else self.player2_color

        # Calculate the x coordinate for the center of the token
        x = col * self.cell_size + self.cell_size // 2

        # Calculate the starting and ending y coordinates for the animation
        start_y = self.cell_size + self.cell_size // 2
        end_y = (target_row + 2) * self.cell_size + self.cell_size // 2
        y = start_y

        # Define the speed of the animation (how many pixels the token moves per frame)
        speed = 20
        clock = pygame.time.Clock()

        # Animate the token falling until it reaches the target row
        while y < end_y:
            # Redraw the board to clear the previous token position
            self.draw_board()

            # Draw the token at the current position
            circle_radius = self.cell_size // 2 - 5
            pygame.draw.circle(self.screen, color, (x, y), circle_radius)

            pygame.display.update()
            y += speed
            if y > end_y:
                y = end_y
            clock.tick(60)

    def fill_row_above_board(self) -> None:
        """Clear the area above the board to remove hover or animation tokens."""
        top_background = pygame.Surface((self.width, self.cell_size))
        top_background.fill(self.bg_color)
        self.screen.blit(top_background, (0, self.cell_size))
        pygame.display.update((0, self.cell_size, self.width, self.cell_size))

    def handle_game_end(self, winner: Optional[int]) -> None:
        """Handle the end of the game, display the result message, and set finished state."""
        self.finished = True

        if not winner:
            self.show_message("It's a tie!")
            return
        if winner == self.player:
            self.show_message("Player won!")
        else:
            self.show_message("AI won!")
