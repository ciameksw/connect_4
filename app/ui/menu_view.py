import pygame

from app.ui import button


class MenuView:
    def __init__(self, screen: pygame.Surface):
        # Initialize menu view with screen, dimensions, and button list
        self.screen = screen
        self.width = 800
        self.height = 600

        self.id = "menu"
        self.start_as_1_id = "start_player_1"
        self.start_as_2_id = "start_player_2"
        self.options_id = "options"

        # UI
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.buttons_font = pygame.font.SysFont("Arial", 32)

        self.bg_color = (25, 55, 110)

        self.text_color = (255, 255, 255)
        self.text_color_darker = (40, 40, 40)

        self.light_blue_color = (50, 150, 220)
        self.yellow_color = (240, 200, 40)
        self.red_color = (220, 50, 50)

        self.menu_buttons = self.setup_buttons()

    def setup_buttons(self) -> list[button.Button]:
        # Define button rectangles
        start_as_player_1_rect = pygame.Rect(self.width // 2 - 150, 160, 300, 80)
        start_as_player_2_rect = pygame.Rect(self.width // 2 - 150, 320, 300, 80)
        options_rect = pygame.Rect(self.width // 2 - 150, 480, 300, 80)

        # Create buttons with their labels and IDs
        start_as_player_1_btn = button.Button(
            start_as_player_1_rect,
            "Start as Player 1",
            self.start_as_1_id,
            self.red_color,
            self.text_color,
        )
        start_as_player_2_btn = button.Button(
            start_as_player_2_rect,
            "Start as Player 2",
            self.start_as_2_id,
            self.yellow_color,
            self.text_color_darker,
        )
        options_btn = button.Button(
            options_rect, "Options", self.options_id, self.light_blue_color, self.text_color
        )

        # Return list of buttons with their labels
        return [start_as_player_1_btn, start_as_player_2_btn, options_btn]

    def show(self) -> None:
        # Fill the background
        self.screen.fill(self.bg_color)

        # Draw the title
        title = self.title_font.render("Connect 4", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)

        # Draw the buttons
        for btn in self.menu_buttons:
            btn.draw(self.screen, self.buttons_font)

        # Update the display to show the menu
        pygame.display.flip()

    def handle_button_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            pos = event.pos

            # Check if any button was clicked
            for button in self.menu_buttons:
                if button.rect.collidepoint(pos):
                    return button.id
        return None
