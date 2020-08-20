# This file contains the Settings class for Alien Invasion

class Settings:
    """
    Settings class to store all of the settings for Alien Invasion
    """

    def __init__(self):
        """
        Initialises static game settings
        """
        # Screen settings

        # The screen has the (0,0) point at the top-left corner
        # x-coordinates increase to the right of the origin
        # y-coordinates increase below the origin
        self.screen_width = 1200
        self.screen_height = 800
        # the point (1200,800) represents the bottom right of our screen
        self.bg_colour = (230,230,230)  # colour matching the ship's background

        # Ship setting

        self.ship_limit = 3

        # Bullet settings

        self.bullets_allowed = 5  # limits how many bullets a player can fire
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60,60,60)

        # Alien setting

        self.fleet_drop_speed = 10
        self.score_scale = 1.1618

        # Game speed up rate

        self.speedup_scale = 1.3

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """
        Initialises settings that change throughout the game
        """

        # Ship setting

        self.ship_speed = 1.5

        # Bullet settings

        self.bullet_speed = 5.0

        # Alien setting

        self.alien_speed = 1.0
        self.fleet_direction = 1  # 1 => fleet to the right; -1 => fleet to the left
        self.alien_points = 10

    def increase_speed(self):
        """
        Increases speed dynamic settings and alien score value
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
