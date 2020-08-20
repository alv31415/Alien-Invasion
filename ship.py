import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_game):
        """
        Manages the ship in alien invasion
        """
        super().__init__()
        self.screen = ai_game.screen  # our ship is displayed in the same surface as the game/background
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # in pygame, objects are managed as RECTangles. This makes it simpler to display and work with
        # we make the ship's screen rectangle be the same as that of the background,
        # as that way we can position it correctly within the screen

        # Load ship image & manage its rectangle
        self.image = pg.image.load("ship.bmp")
        self.rect = self.image.get_rect()  # the rectangle of the ship itself is determined by the picture that represents it

        # Place a ship in the bottom centre of the screen
        self.rect.midbottom = self.screen_rect.midbottom  # we place the ship in the bottom centre of the game screen

        # Store horizontal position of ship
        self.x = float(self.rect.x)

        # Flags for continuous movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Update the ship's position based on the movement flag
        Allows continuous movement if the arrow keys are pressed continuously
        """
        if (self.moving_right) and (self.rect.right < self.screen_rect.right):  # limit ship's movement so it doesn't go off screen
            self.x += self.settings.ship_speed
        if (self.moving_left) and (self.rect.left > 0):
            self.x -= self.settings.ship_speed
        self.rect.x = self.x  # update the rectangle's position once the ship has moved

    def blitme(self):
        """
        Draw the ship at its location
        """
        self.screen.blit(self.image, self.rect)  # blit draws the image at the specified rectangle

    def center_ship(self):
        """
        Center ship on screen
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)