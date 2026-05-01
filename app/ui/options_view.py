import pygame
from pygame.event import Event


class OptionsView:
    def __init__(self, screen, font, config):
        # Initialize options view with screen, font, dimensions, and config
        self.screen = screen
        self.font = font
        self.width = 800
        self.cell_size = 80
        self.config = config
        self.id = "options"

        self.options_font = pygame.font.SysFont("Arial", 20)

        # Define options for editing
        self.options = [
            ("rows", int),
            ("columns", int),
            ("win_length", int),
            ("minimax_search_depth", int),
            ("heuristic_score_exact_win_length", float),
            ("heuristic_score_one_missing", float),
            ("heuristic_score_two_missing", float),
            ("heuristic_score_three_missing", float),
            ("heuristic_penalty_opponent_one_missing", float),
            ("heuristic_penalty_opponent_two_missing", float),
            ("heuristic_penalty_opponent_three_missing", float),
            ("heuristic_score_center_column", float),
            ("heuristic_score_multiplier", float),
            ("heuristic_depth_discount_ratio", float),
            ("terminal_score_win", float),
            ("terminal_score_loss", float),
        ]

        # Editing state
        self.selected_index = 0
        self.edit_mode = False
        self.input_buffer = ""

    def show(self):
        # Fill the background
        self.screen.fill((255, 255, 255))

        # Show message to press ESC to go back to menu
        esc = self.font.render("Press ESC to go back to menu", True, (0, 0, 0))
        esc_rect = esc.get_rect(center=(self.width // 2, self.cell_size * 0.5))
        self.screen.blit(esc, esc_rect)

        # Display the title
        title = self.font.render("Options", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.cell_size * 1.2))
        self.screen.blit(title, title_rect)

        # Display the options
        y = 120
        line_height = self.options_font.get_height() + 8
        for i, (key, _) in enumerate(self.options):
            value = getattr(self.config, key)

            # Highlight the selected option
            color = (200, 0, 0) if i == self.selected_index else (0, 0, 0)

            # Show input buffer if in edit mode
            if self.edit_mode and i == self.selected_index:
                text = f"{key}: {self.input_buffer}_"
            else:
                text = f"{key}: {value}"

            # Render the option text
            label = self.options_font.render(text, True, color)
            self.screen.blit(label, (50, y))
            y += line_height

        # Update the display to show the options
        pygame.display.flip()

    def handle_event_in_select_mode(self, event: Event):
        # In select mode, we navigate the options and enter edit mode
        if event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            key, _ = self.options[self.selected_index]
            self.input_buffer = str(getattr(self.config, key))
            self.edit_mode = True

    def handle_event_in_edit_mode(self, event: Event):
        # In edit mode, we capture input for the selected option and save it on Enter
        if event.key == pygame.K_RETURN:
            # Get the key and expected type for the selected option
            key, value_type = self.options[self.selected_index]

            # Try to convert the input buffer to the expected type and save it in the config
            try:
                new_value = value_type(self.input_buffer)
                setattr(self.config, key, new_value)
            except ValueError:
                pass
            self.edit_mode = False
        elif event.key == pygame.K_BACKSPACE:
            # Remove the last character from the input buffer
            self.input_buffer = self.input_buffer[:-1]
        else:
            # Only allow digits, decimal point, and minus sign in the input buffer
            if event.unicode.isdigit() or event.unicode in ".-":
                self.input_buffer += event.unicode
