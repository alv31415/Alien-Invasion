import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    Class representing an alien
    """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien and set up rect
        self.image = pg.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # Aliens begin at top left of the screen
        self.rect.x = self.rect.width  # allows sufficient lateral distance
        self.rect.y = self.rect.height  # allows sufficient vertical distance

        # Store alien's horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """
        Move alien right or left
        """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """
        True if an alien is at the edge of the screen
        """
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)