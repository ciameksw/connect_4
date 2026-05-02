from dataclasses import dataclass

import pygame


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    id: str
    color: tuple[int, int, int]
    text_color: tuple[int, int, int]

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
