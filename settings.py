import os
import json

from game_config import config as default_config


class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self, base_path):
        """Initialize the game's settings"""
        # Set base path
        self.base_path = base_path

        # Load the configuration
        self.get_config()

        # Screen settings
        self.screen_width = self.config['screen_width']
        self.screen_height = self.config['screen_height']
        self.bg_color = self.config['bg_color']

        # Ship settings
        # how many ships the player has at the start of the game
        self.ship_limit = self.config['ship_limit']

        # Bullet settings
        self.bullet_width = self.config['bullet_width']
        self.bullet_height = self.config['bullet_height']
        self.bullet_color = self.config['bullet_color']
        # how many bullets are allowed to on the screen at the same time
        self.bullets_allowed = self.config['bullets_allowed']

        # Alien settings
        # how fast the aliens move down the screen
        self.fleet_drop_speed = self.config['fleet_drop_speed']

        # How quickly the game speeds up
        self.speedup_scale = self.config['speedup_scale']

        # How quickly the alien point values increase
        self.score_scale = self.config['score_scale']


    def init_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        # Speed values
        self.ship_speed = self.config['ship_speed']
        self.bullet_speed = self.config['bullet_speed']
        self.alien_speed = self.config['alien_speed']

        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = self.config['alien_points']


    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def get_config(self):
        """
        Load the the game's settings' configuration from config.json.
        Get the default configuration if the config file is missing and save the config
        """
        config_file_path = os.path.join(self.base_path, 'config.json')
        try:
            with open(config_file_path) as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError or json.JSONDecodeError:
            self.config = default_config
            with open(config_file_path, 'w') as config_file:
                json.dump(default_config, config_file)
