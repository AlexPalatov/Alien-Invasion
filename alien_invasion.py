import pygame
from pygame.sprite import Group
from pygame.mixer import Sound

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Initialize game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # Load sounds
    shot_sound = Sound('sounds/shot.wav')
    collision_sound = Sound('sounds/collision.wav')
    alien_death_sound = Sound('sounds/alien_destruction.wav')
    level_up_sound = Sound('sounds/level_up.wav')
    game_over_sound = Sound('sounds/game_over.wav')
    pygame.mixer_music.load('sounds/background.wav')

    # Make a ship
    ship = Ship(screen, ai_settings)

    # Make a group to store bullets in
    bullets = Group()

    # Make a fleet of aliens
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, scoreboard, play_button,
                        ship, aliens, bullets, shot_sound)
        if stats.game_active and not stats.pause:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard,
                              ship, aliens, bullets,
                              alien_death_sound, level_up_sound)
            gf.update_aliens(ai_settings, stats, screen, scoreboard,
                             ship, aliens, bullets, collision_sound, game_over_sound)
        gf.update_screen(ai_settings, screen, stats, scoreboard,
                         ship, aliens, bullets, play_button)


run_game()
