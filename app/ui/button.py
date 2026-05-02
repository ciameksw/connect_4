from dataclasses import dataclass

import pygame


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    id: str
    color: tuple
    text_color: tuple
