import pygame
from pygame.event import Event

from app.ui import button


class OptionsView:
    def __init__(self, screen, config):
        # Initialize options view with screen, dimensions, and config
        self.screen = screen
        self.width = 800
        self.height = 600
        self.cell_size = 80
        self.config = config
        self.id = "options"

        self.options_font = pygame.font.SysFont("Arial", 20)

        self.easy_id = "easy"
        self.medium_id = "medium"
        self.hard_id = "hard"
        self.options_buttons = self.setup_buttons()

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

    def setup_buttons(self):
        button_width = 180
        button_height = 50
        spacing = 40

        x = 530
        start_y = 80

        # Define button rectangles
        easy_rect = pygame.Rect(x, start_y, button_width, button_height)
        medium_rect = pygame.Rect(x, start_y + button_height + spacing, button_width, button_height)
        hard_rect = pygame.Rect(
            x, start_y + 2 * (button_height + spacing), button_width, button_height
        )

        # Create buttons with their labels and IDs
        easy_btn = button.Button(easy_rect, "Easy", self.easy_id, (60, 180, 90), (255, 255, 255))
        medium_btn = button.Button(
            medium_rect, "Medium", self.medium_id, (240, 200, 40), (40, 40, 40)
        )
        hard_btn = button.Button(hard_rect, "Hard", self.hard_id, (200, 60, 60), (255, 255, 255))

        # Return list of buttons with their labels
        return [easy_btn, medium_btn, hard_btn]

    def show(self):
        # Fill the background
        self.screen.fill((30, 80, 160))

        # Show message to press ESC to go back to menu
        esc = pygame.font.SysFont("Arial", 24).render("ESC - Go Back", True, (255, 255, 255))
        esc_rect = esc.get_rect(center=(80, 40))
        self.screen.blit(esc, esc_rect)

        # Display the title
        title = pygame.font.SysFont("Arial", 40).render("Options", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)

        # Draw the buttons
        for btn in self.options_buttons:
            btn.draw(self.screen, pygame.font.SysFont("Arial", 32))

        # Display the options
        self.show_options()

        # Update the display to show the options
        pygame.display.flip()

    def show_options(self):
        y = 80
        line_height = self.options_font.get_height() + 8
        for i, (key, _) in enumerate(self.options):
            value = getattr(self.config, key)

            if i == self.selected_index:
                # Red for selected option, yellow if in edit mode
                color = (255, 255, 0) if self.edit_mode else (200, 0, 0)
            else:
                color = (255, 255, 255)  # White for non-selected options

            # Show input buffer if in edit mode
            if self.edit_mode and i == self.selected_index:
                text = f"{key}: {self.input_buffer}_"
            else:
                text = f"{key}: {value}"

            # Render the option text
            label = self.options_font.render(text, True, color)
            self.screen.blit(label, (50, y))
            y += line_height

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
