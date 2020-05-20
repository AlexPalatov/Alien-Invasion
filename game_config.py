"""Default configuration for the game"""
config = {
    # Screen settings
    'screen_width': 1200,
    'screen_height': 800,
    'bg_color': (230, 230, 230),

    # Ship settings
    'ship_speed': 1.5,
    'ship_limit': 3,

    # Bullet settings
    'bullet_width': 3,
    'bullet_height': 15,
    'bullet_color': (200, 150, 60),
    'bullets_allowed': 3,
    'bullet_speed': 1.5,

    # Alien settings
    'alien_speed': 1,
    'fleet_drop_speed': 10,

    # Scoring and difficulty
    'speedup_scale': 1.1,
    'score_scale': 1.5,
    'alien_points': 10,
}
