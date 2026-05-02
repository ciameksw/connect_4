import pygame

from app.ui.button import Button


class MenuView:
    def __init__(self, screen):
        # Initialize menu view with screen, dimensions, and button list
        self.screen = screen
        self.width = 800
        self.height = 600

        self.id = "menu"
        self.start_as_1_id = "start_player_1"
        self.start_as_2_id = "start_player_2"
        self.options_id = "options"
        self.menu_buttons = self.setup_buttons()

    def setup_buttons(self):
        # Define button rectangles
        start_as_player_1_rect = pygame.Rect(self.width // 2 - 150, 160, 300, 80)
        start_as_player_2_rect = pygame.Rect(self.width // 2 - 150, 320, 300, 80)
        options_rect = pygame.Rect(self.width // 2 - 150, 480, 300, 80)

        # Create buttons with their labels and IDs
        start_as_player_1_btn = Button(
            start_as_player_1_rect,
            "Start as Player 1",
            self.start_as_1_id,
            (220, 40, 40),
            (255, 255, 255),
        )
        start_as_player_2_btn = Button(
            start_as_player_2_rect,
            "Start as Player 2",
            self.start_as_2_id,
            (240, 200, 40),
            (40, 40, 40),
        )
        options_btn = Button(
            options_rect, "Options", self.options_id, (50, 150, 220), (255, 255, 255)
        )

        # Return list of buttons with their labels
        return [start_as_player_1_btn, start_as_player_2_btn, options_btn]

    def show(self):
        # Fill the background
        self.screen.fill((30, 80, 160))

        # Draw the title
        title = pygame.font.SysFont("Arial", 64).render("Connect 4", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)

        # Draw the buttons
        for button in self.menu_buttons:
            pygame.draw.rect(self.screen, button.color, button.rect)
            label = pygame.font.SysFont("Arial", 32).render(button.text, True, button.text_color)
            label_rect = label.get_rect(center=button.rect.center)
            self.screen.blit(label, label_rect)

        # Update the display to show the menu
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            pos = event.pos

            # Check if any button was clicked
            for button in self.menu_buttons:
                if button.rect.collidepoint(pos):
                    return button.id
        return None
