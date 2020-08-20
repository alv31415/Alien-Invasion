import sys  # manage system responses
import pygame as pg  # build the game
from time import sleep  # functionality for time keeping
import os.path

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# We create a class that will control the main game

class AlienInvasion:
    """
    Manages the game's assets and behaviour
    """

    def __init__(self):
        """
        Initialises the game and creates its resources
        """
        pg.init()
        self.settings = Settings()  # we specify settings within the instance, and these get applied to the game

        self.screen = pg.display.set_mode(
          (self.settings.screen_width, self.settings.screen_height))  # creates the game SURFACE to display stuff
           # it takes in a tuple that specifies the width and height
        pg.display.set_caption("Alien Invasion")  # sets the title of the window

        # Create instance of GameStatistics and Scoreboard to keep up
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        if not os.path.exists(self.stats.my_scores):
            self.stats.create_high_score_json()

        self.ship = Ship(self)  # initialise ship to be part of this game
        self.bullets = pg.sprite.Group()  # bullets is a group that will contain all the bullets that are fired
        # Group is a useful class that will allow us to manipulate all the bullets at once
        self.aliens = pg.sprite.Group()

        self._create_fleet()

         # Main Title Buttons

        self.title = Button(self, "Alien Invasion")
        self.title._prep_button_to_title()

        self.play_button = Button(self, "Play")

        self.high_score_button = Button(self, "High-Scores")
        self.high_score_button._change_rect_to(self.play_button.screen_rect.centerx, self.play_button.screen_rect.centery + 100)

        self.instructions_button = Button(self, "Instructions")
        self.instructions_button._change_rect_to(self.play_button.screen_rect.centerx, self.play_button.screen_rect.centery + 200)

        # Next level flag

        self.is_next_level = False

        # Instructions flag

        self.is_instructions_pane = False

        # High Scores flag

        self.is_high_score_pane = False

    def run_game(self):
        """
        Executes the main loop of the game
        """
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):  # the underscore at the beginning indicates that this is a helper method
        """
        Helper method used to handle any event triggered by the user, such as the ship's movement
        """
        for event in pg.event.get():  # checks any event caused by user
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()  # if we click the exit button, exit the game
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_instructions_button(mouse_pos)
                self._check_scores_button(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pg.KEYDOWN:  # checks if user presses a key
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if (event.key == pg.K_RIGHT) and (not self.is_next_level) :  # checks if the key pressed is the right arrow
            self.ship.moving_right = True  # allows the ship to continuously update position if the key is pressed down
        elif (event.key == pg.K_LEFT) and (not self.is_next_level):
            self.ship.moving_left = True
        elif (event.key == pg.K_SPACE) and (not self.is_next_level):
            self._fire_bullet()
        elif (event.key == pg.K_q) or (event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.key == pg.K_x:
            self.settings.fleet_drop_speed = 150
        elif event.key == pg.K_g:
            self.settings.bullet_speed = 20
            self.settings.ship_speed = 10
        elif (event.key == pg.K_RETURN) and (self.is_next_level):
            self.is_next_level = False
            self.settings.alien_speed = 1
            sleep(0.5)
        elif event.key == pg.K_BACKSPACE:
            self.is_instructions_pane = False
            self.is_high_score_pane = False

    def _check_keyup_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_colour)
        if self.stats.game_active:
            self.ship.blitme()
            self.sb.show_score()
            if self.is_next_level:
                self.settings.alien_speed = 0
                next_level = Button(self,f"Level {self.stats.level}")
                next_level._prep_button_to_message()
                next_level.draw_button()
            else:
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
        else:
            if self.is_instructions_pane:
                self.sb.draw_instructions()
            elif self.is_high_score_pane:
                self.sb.draw_high_scores()
            else:
                self.title.draw_button()
                self.play_button.draw_button()
                self.high_score_button.draw_button()
                self.instructions_button.draw_button()

        pg.display.flip()

    def _fire_bullet(self):
        """
        Create new bullet, adding it to bullets
        """
        if len(self.bullets) < self.settings.bullets_allowed:  # can only fire a certain amount of bullets at a time
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)  # the create dbullet gets added to our group

    def _remove_bullets(self):
        """
        Removes off screen bullets
        """
        for bullet in self.bullets.copy():  # make a copy that we can go through to see which bullets to remove
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_bullets(self):
        """
        Updates the position of bullets, removing old ones
        """
        self.bullets.update()  # Group allows us to update each sprite within bullets
        self._remove_bullets()
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # We check to see if any bullet has collided with an alien using the method groupcollide()
        # This checks whether the sprites of 2 groups have collided, by checking their rectnalges
        # It returns a dictionary, containing sprites as the key value pairs
        # We can spcify whether we want the sprites to disappear
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)  # bullets are key; aliens are values
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Eliminate old bullet and repopulate the fleet, increasing speed settings for next level
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.is_next_level = True
            self.sb.prep_level()
            self.settings.alien_speed = 0

    def _create_fleet(self):
        """
        Creates a feet of aliens
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Determine aliens in a row
        available_space_x = self.settings.screen_width - (2*alien_width)  # we leave a margin of one alien
        number_aliens_x = available_space_x // (2*alien_width) # we leave a space of one alien in between each alien
        # // is the floor division operator, which applies the floor function to a division

        # Determine rows in screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)

        # Create a fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number, row_number):
        """
        Used to create aliens in a row using a for loop in _create_fleet()
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Updates the position of all aliens
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check alien-ship collision
        if pg.sprite.spritecollideany(self.ship, self.aliens):  # cehcks if there is any alien that touches the ship
            self._ship_hit()

        # Check alien touching bottom
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """
        Changes direction of movement of fleet if an alien touches an edge
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        Drop the fleet and changes direction
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= - 1

    def _ship_hit(self):
        """
        Responds to the ship being hit by an alien
        """

        if self.stats.ships_left > 0:
            # Decrease ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Remove remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1.0)
        else:
            self.stats.update_high_scores()
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """
        Checks if aliens have reached the bottom of the screen
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """
        Checks that the player clicks the play button
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # check whether the click coordinate is within the rect of the button
        in_menu = self.stats.game_active or self.is_high_score_pane or self.is_instructions_pane
        if button_clicked and not in_menu:  # resets everything if and only if the game is inactive
            self.settings.initialise_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Remove aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # New fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide cursor
            pg.mouse.set_visible(False)

            self.is_next_level = True

    def _check_instructions_button(self, mouse_pos):
        """
        Checks that the player clicks the play button
        """
        button_clicked = self.instructions_button.rect.collidepoint(mouse_pos)
        in_menu = self.stats.game_active or self.is_high_score_pane
        if button_clicked and not in_menu:
            self.is_instructions_pane = True

    def _check_scores_button(self, mouse_pos):
        """
        Checks that the player clicks the high-score button
        """
        button_clicked = self.high_score_button.rect.collidepoint(mouse_pos)
        in_menu = self.stats.game_active or self.is_instructions_pane
        if button_clicked and not in_menu:
            self.is_high_score_pane = True


if __name__ == "__main__":  # run game only if we call the file directly
    ai = AlienInvasion()
    ai.run_game()


