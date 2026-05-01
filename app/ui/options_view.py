import pygame


class OptionsView:
    def __init__(self, screen, font, width, cell_size, config):
        # Initialize options view with screen, font, dimensions, and config
        self.screen = screen
        self.font = font
        self.width = width
        self.cell_size = cell_size
        self.config = config
        self.id = "options"

        # Define options for editing
        self.options = [
            ("rows", int),
            ("columns", int),
            ("win_length", int),
            ("minimax_search_depth", int),
        ]

    def show(self):
        # Fill the background
        self.screen.fill((255, 255, 255))

        # Display the title
        title = self.font.render("Options", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.cell_size))
        self.screen.blit(title, title_rect)

        # Display the options
        y = self.cell_size * 2
        for key, _ in self.options:
            value = getattr(self.config, key)
            label = self.font.render(f"{key}: {value}", True, (0, 0, 0))
            self.screen.blit(label, (self.width // 2 - 100, y))
            y += self.cell_size

        # Update the display to show the options
        pygame.display.flip()
