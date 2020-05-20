import sys
import pygame

from bullet import Bullet
from alien import Alien


def check_keydown(event, ai_settings, screen, stats, scoreboard, ship, aliens, bullets, shot_sound):
    """Respond to key presses"""
    # Ship controls are disabled when then the game is not running
    controls_enabled = stats.game_active and not stats.pause
    if event.key == pygame.K_a or event.key == pygame.K_LEFT and controls_enabled:
        ship.moving_left = True
    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and controls_enabled:
        ship.moving_right = True
    elif event.key == pygame.K_SPACE and controls_enabled:
        fire_bullet(ai_settings, screen, ship, bullets, shot_sound)
    elif event.key == pygame.K_q and not controls_enabled:
        exit_game(stats)
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
    elif event.key == pygame.K_ESCAPE and stats.game_active:
        switch_pause_mode(stats)


def check_keyup(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = False


def check_events(ai_settings, screen, stats, scoreboard, play_button,
                 ship, aliens, bullets, shot_sound):
    """Respond to key and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game(stats)

        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, stats, scoreboard,
                          ship, aliens, bullets, shot_sound)

        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def exit_game(stats):
    """Save high score and exit"""
    stats.save_high_score()
    sys.exit()


def switch_pause_mode(stats):
    """Pause or resume the game"""
    if stats.pause:
        # Resume the game
        stats.pause = False
        pygame.mouse.set_visible(False)
        pygame.mixer_music.play(-1)
    else:
        # Pause the game
        stats.pause = True
        pygame.mouse.set_visible(True)
        pygame.mixer_music.stop()


def check_play_button(ai_settings, screen, stats, scoreboard, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """Start a new game"""
    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Switch off the pause mode
    stats.pause = False

    # Reset the game settings
    ai_settings.init_dynamic_settings()

    # Reset the game statistics
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images
    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    # Remove all aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet amd center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Play background music
    pygame.mixer_music.play(-1)


def fire_bullet(ai_settings, screen, ship, bullets, shot_sound):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        # Play shot sound
        shot_sound.play()

        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, scoreboard,
                   ship, aliens, bullets, alien_death_sound, level_up_sound):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien
    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard,
                                  ship, aliens, bullets,
                                  alien_death_sound, level_up_sound)


def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard,
                                  ship, aliens, bullets,
                                  alien_death_sound, level_up_sound):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # Make sure we handle all hits
        for aliens in collisions.values():
            # Play the sound
            alien_death_sound.play()
            # Increment score
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    # Check if all aliens have been destroyed
    if len(aliens) == 0:
        # Play level up sound
        level_up_sound.play()

        # Destroy existing bullets, speed up the game, and start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        scoreboard.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, scoreboard):
    """Check if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - ship_height - 5 * alien_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_width, alien_height):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)

    # Set the x position
    alien.x = 0.7 * alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x

    # Set the y position
    alien.rect.y = 3 * alien_height + 1.5 * alien_height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is half the alien width
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien_height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_width, alien_height)


def check_fleet_edges(ai_settings, aliens):
    """Call change_fleet direction if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop down the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, scoreboard,
             ship, aliens, bullets, collision_sound, game_over_sound):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # Wait until the collision sound has been played
        collision_sound.play()
        while pygame.mixer.get_busy():
            pass

        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard
        scoreboard.prep_ships()

        # Destroy all aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    else:
        # Stop the game and make the cursor reappear
        game_over_sound.play()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        pygame.mixer_music.stop()


def check_aliens_bottom(ai_settings, stats, screen, scoreboard,
                        ship, aliens, bullets,
                        collision_sound, game_over_sound):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this as if the ship was hit
            ship_hit(ai_settings, stats, screen, scoreboard,
                     ship, aliens, bullets, collision_sound, game_over_sound)
            break


def update_aliens(ai_settings, stats, screen, scoreboard,
                  ship, aliens, bullets,
                  collision_sound, game_over_sound):
    """
    Check if the fleet is at an edge
    and then update the positions of all the aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, scoreboard,
                 ship, aliens, bullets,
                 collision_sound, game_over_sound)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, scoreboard,
                        ship, aliens, bullets,
                        collision_sound, game_over_sound)


def update_screen(ai_settings, screen, stats, scoreboard,
                  ship, aliens, bullets, play_button, bg_image):
    """Update images on the screen and flip to the new screen"""
    # Disable the timer if it's active

    # Redraw the screen during each pass through the loop
    #screen.fill(ai_settings.bg_color)
    screen.blit(bg_image, (0, 0))

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw()

    # Redraw ship and aliens
    ship.blitme()
    aliens.draw(screen)

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw()

    # Draw the scoreboard
    scoreboard.show_score()

    # Make the most recently drawn screen visible
    pygame.display.flip()
