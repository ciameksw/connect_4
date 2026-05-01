from dataclasses import dataclass

import pygame


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    id: str


class MenuView:
    def __init__(self, screen, font):
        # Initialize menu view with screen, font, dimensions, and button list
        self.screen = screen
        self.font = font
        self.width = 800
        self.cell_size = 80
        self.id = "menu"
        self.start_as_1_id = "start_player_1"
        self.start_as_2_id = "start_player_2"
        self.options_id = "options"
        self.menu_buttons = self.setup_buttons()

    def setup_buttons(self):
        # Define button rectangles
        start_as_player_1_rect = pygame.Rect(
            self.width // 2 - 150, self.cell_size * 2, 300, self.cell_size
        )
        start_as_player_2_rect = pygame.Rect(
            self.width // 2 - 150, self.cell_size * 4, 300, self.cell_size
        )
        options_rect = pygame.Rect(self.width // 2 - 150, self.cell_size * 6, 300, self.cell_size)

        # Create buttons with their labels and IDs
        start_as_player_1_btn = Button(
            start_as_player_1_rect, "Start as Player 1", self.start_as_1_id
        )
        start_as_player_2_btn = Button(
            start_as_player_2_rect, "Start as Player 2", self.start_as_2_id
        )
        options_btn = Button(options_rect, "Options", self.options_id)

        # Return list of buttons with their labels
        return [start_as_player_1_btn, start_as_player_2_btn, options_btn]

    def show(self):
        # Fill the background
        self.screen.fill((255, 255, 255))

        # Draw the title
        title = self.font.render("Connect 4", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.cell_size))
        self.screen.blit(title, title_rect)

        # Draw the buttons
        for button in self.menu_buttons:
            pygame.draw.rect(self.screen, (200, 200, 200), button.rect)
            label = self.font.render(button.text, True, (0, 0, 0))
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
