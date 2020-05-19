import json


class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

        # Switch off the pause mode
        self.pause = False

    def load_high_score(self):
        """
        Restore high score from the score.json file
        Return 0 if no score is saved
        """
        try:
            with open('score.json', 'r') as high_score_file:
                high_score = json.load(high_score_file)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError:
            return 0
        else:
            return high_score

    def save_high_score(self):
        """Save high score to the file score.json"""
        with open('score.json', 'w') as high_score_fle:
            json.dump(self.high_score, high_score_fle)
