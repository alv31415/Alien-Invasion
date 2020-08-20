import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    Child class of Sprite
    The Sprite class allows us to group related elements, and act on all of them at once
    Manages bullets and behaviour
    """

    def __init__(self, ai_game):
        """
        Create bullet object at ship's position
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        # Create the bulet rect at (0,0) and thenstranslate it above the ship's position
        self.rect = pg.Rect(0,0,self.settings.bullet_width, self.settings.bullet_height)  # creates rectangle with bullet dimensions
        self.rect.midtop = ai_game.ship.rect.midtop  # places bullet above the ship

        # Store bullet position
        self.y = float(self.rect.y)

    def update(self):
        """
        Moves the bullet up the screen when shot
        """
        self.y -= self.settings.bullet_speed  # update bullet position
        self.rect.y = self.y  # update its rectangle

    def draw_bullet(self):
        """
        Draw bullet into screen
        """
        pg.draw.rect(self.screen, self.colour,self.rect)  # draws a rectangle in a given screen, with our bullet colour and on our rectangle