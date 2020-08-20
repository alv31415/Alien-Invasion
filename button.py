import pygame as pg
import pygame.font as pgf

class Button:
    def __init__(self, ai_game, msg):
        self.msg = msg
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Properties of the button
        self.width, self.height = 250,50
        self.button_colour = (0,255,0)
        self.text_colour = (255,255,255)
        self.font = pgf.SysFont(None,48)

        # Build Rect object
        self.rect = pg.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # Add message
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """
        Turn msg into rendered image and center text
        """
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)  # font render turns text into an image
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _prep_button_to_message(self):
        # Properties of the message
        self.width, self.height = 400, 200
        self.text_colour = (255, 255, 255)
        self.button_colour = (0, 0, 0)
        self.font = pgf.SysFont(None, 80)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center


        self._prep_msg(self.msg)

    def _prep_button_to_title(self):
        # Properties of the message
        self.width, self.height = 800, 200
        self.text_colour = (0, 0, 0)
        self.button_colour = self.settings.bg_colour
        self.font = pgf.SysFont("Times", 100,True)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.screen_rect.centerx,self.screen_rect.centery//2)

        self._prep_msg(self.msg)

    def _change_rect_to(self,x,y):
        self.rect.center = (x,y)
        self._prep_msg(self.msg)

    def draw_button(self):
        """
        Draw button and write message
        """
        self.screen.fill(self.button_colour,self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)