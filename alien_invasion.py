import os
import pygame
from pygame.sprite import Group
from pygame.mixer import Sound

from ship import Ship
from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings(os.path.dirname(__file__))
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Initialize game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # Load background image
    bg_image_path = os.path.join(os.path.dirname(__file__), 'images/background_2.0.bmp')
    bg_image = pygame.image.load(bg_image_path)

    # Load sounds
    file_path = os.path.dirname(__file__)
    shot_sound = Sound(os.path.join(file_path, 'sounds/shot.wav'))
    collision_sound = Sound(os.path.join(file_path,'sounds/collision.wav'))
    alien_death_sound = Sound(os.path.join(file_path, 'sounds/alien_destruction.wav'))
    level_up_sound = Sound(os.path.join(file_path, 'sounds/level_up.wav'))
    game_over_sound = Sound(os.path.join(file_path, 'sounds/game_over.wav'))
    pygame.mixer_music.load(os.path.join(file_path, 'sounds/background.wav'))

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
                              alien_death_sound, level_up_sound, bg_image)
            gf.update_aliens(ai_settings, stats, screen, scoreboard,
                             ship, aliens, bullets,
                             collision_sound, game_over_sound)
        gf.update_screen(ai_settings, screen, stats, scoreboard,
                         ship, aliens, bullets, play_button, bg_image)


run_game()
