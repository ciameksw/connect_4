from typing import Optional

import pygame


class GameView:
    def __init__(self, screen, font, width, height, cell_size, config, game_logic):
        # Initialize game view with screen, font, dimensions, config, and game logic
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.config = config
        self.game_logic = game_logic
        self.id = "game"

        # By default the player is player 1, but this can be changed in the menu
        self.player = self.config.player1

    def reset_game(self, player: int):
        # Set the player
        self.player = player

        # Create a new board
        self.board = self.game_logic.create_board()

        # Set game state variables
        self.current_player = self.config.player1
        self.finished = False
        self.last_move = None

    def show_message(self, message: str):
        # Create white overlay
        overlay = pygame.Surface((self.width, self.cell_size))
        overlay.fill((255, 255, 255))

        # Add text
        text = self.font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.cell_size // 2))
        overlay.blit(text, text_rect)

        # Display the overlay on the screen
        self.screen.blit(overlay, (0, 0))

        # Update the display to show the message
        pygame.display.flip()

    def get_column_from_mouse(self, pos: tuple[int, int]) -> Optional[int]:
        x, _ = pos

        # Convert x coordinate to column index
        col = x // self.cell_size

        # Check if the column index is within bounds
        if 0 <= col < self.config.columns:
            return col
        return None

    def draw_board(self):
        # Fill the background with blue
        self.screen.fill((0, 0, 255))

        # Top of the screen stays white
        overlay = pygame.Surface((self.width, self.cell_size * 2))
        overlay.fill((255, 255, 255))
        self.screen.blit(overlay, (0, 0))

        # Show message to press ESC to go back to menu
        self.show_message("Press ESC to go back to menu")

        # For each cell
        for r in range(self.config.rows):
            for c in range(self.config.columns):
                # Get the coordinates of the left, top corner of the cell
                x = c * self.cell_size
                y = (r + 2) * self.cell_size

                # Determine the color based on the cell value
                color = (255, 255, 255)
                if self.board[r][c] == self.config.player1:
                    color = (255, 0, 0)
                elif self.board[r][c] == self.config.player2:
                    color = (255, 255, 0)

                # Draw a circle in the cell with the determined color
                circle_center = (x + self.cell_size // 2, y + self.cell_size // 2)
                circle_radius = self.cell_size // 2 - 5
                pygame.draw.circle(self.screen, color, circle_center, circle_radius)

        # Update the display to show the new board
        pygame.display.flip()

    def handle_move(self, col: int):
        # Make the move for provided column
        move_result = self.game_logic.make_move(self.board, col, self.current_player)

        # Update game state
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

    def handle_game_end(self, winner: Optional[int]):
        # Set game to finished
        self.finished = True

        # Show appropriate message based on winner
        if not winner:
            self.show_message("It's a tie!")
            return
        if winner == self.player:
            self.show_message("Player won!")
        else:
            self.show_message("AI won!")
