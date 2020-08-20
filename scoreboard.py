import pygame.font as pgf
import json
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """
    Class reporting point information
    """

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_colour = (30, 30, 30)
        self.font = pgf.SysFont(None, 48)

        # Prepare the score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)  # inserts commas for large numbers (i.e 1,000 instead of 1000)
        self.score_image = self.font.render(score_str, True, self.text_colour, self.settings.bg_colour)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.settings.bg_colour)

        # Display high score at the centre of the screen

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """
        Check if there's a new high score
        """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_colour, self.settings.bg_colour)

        # Position level below score

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """
        Shows the ships available
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def multi_render(self, line_array, x, y):

        rendered = []
        self.font = pgf.SysFont("Times", 48)

        for line in line_array:
            rendered.append(self.font.render(line, True, self.text_colour, self.settings.bg_colour))

        posY = self.score_rect.top + 100

        for i in range(len(rendered)):
            render_rect = (x, y + 60 * i)
            self.screen.blit(rendered[i], render_rect)

    def draw_instructions(self):
        """
        Displays instructions
        """

        self.make_title("Instructions")

        instructions = ["Welcome to Alien Invasion!",
                        "Move the ship by pressing the left and right arrow keys.",
                        "Press the spacebar to shoot bullets at the aliens.",
                        "Press enter when a level is finished to continue",
                        "to the next level.",
                        "You lose a life if an alien touches your ship, or passes you.",
                        "If you lose 3 lives, the game is over.",
                        "Press backspace to return to the menu."]

        self.multi_render(instructions, self.screen_rect.centerx - 500, self.score_rect.top + 100)

    def draw_high_scores(self):
        """
        Displays high-scores
        """

        self.make_title("High-Scores")

        scores_dict = {}
        scores_array = []

        try:
            with open(self.stats.my_scores, "r") as f:
                scores_dict = json.load(f)
        except FileNotFoundError:
            self.stats.create_high_score_json()

        for key, value in scores_dict.items():
            scores_array.append(f"{key}:  {value}")

        self.multi_render(scores_array, self.screen_rect.centerx - 100, self.score_rect.top + 100)

    def make_title(self,msg):
        """
        Creates titles
        """
        self.font = pgf.SysFont("Times", 60, True)
        self.score_title = self.font.render(msg, True, self.text_colour, self.settings.bg_colour)

        self.score_title_rect = self.score_title.get_rect()
        self.score_title_rect.x = self.screen_rect.centerx - 150
        self.score_title_rect.y = self.screen_rect.top + 50

        self.screen.blit(self.score_title, self.score_title_rect)

    def show_score(self):
        """
        Draws score to the screen
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
