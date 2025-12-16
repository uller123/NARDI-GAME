import pygame
from Game import *
from Initer import *


def start_game(my_screen, my_clock):
    game_state = GameState()
    game_state.screen = my_screen
    game_state.clock = my_clock
    return main_game_loop(game_state)


def initialize_game(game_state):
    dec = pygame.transform.scale(
        pygame.image.load("Images/доска.png"),
        (600, 600))
    cube = Cube()
    init_bases(game_state)
    skip_butt = SkipButton()
    was_move = False
    return dec, cube, skip_butt, was_move


def handle_events(game_state, cube):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not game_state.cubs_was_trow:
            game_state.cubes_num = cube.throw_cubs(game_state.screen, game_state.clock)
            game_state.cubs_was_trow = True
        if keys[pygame.K_ESCAPE]:
            return "None"
    return None


def check_game_over(game_state):
    if game_state.count_of_black >= 1 and not game_state.move_is_going:
        return "Black"
    if game_state.count_of_white >= 1 and not game_state.move_is_going:
        return "White"
    return None


def update_game_state(game_state, was_move):
    new_was_move = was_move

    if game_state.move_is_going and not was_move:
        new_was_move = True
    elif not game_state.move_is_going and was_move:
        new_was_move = False
        game_state.move_index += 1
        if game_state.move_index == 2:
            game_state.move_index = 0
            if game_state.move_color == "Black":
                game_state.move_color = "White"
            else:
                game_state.move_color = "Black"
            game_state.cubs_was_trow = False
    return new_was_move


def render_game(game_state, dec, skip_butt, cube):
    game_state.screen.blit(dec, (0, 0))
    skip_butt.check_mouse(game_state)

    for base in game_state.baseList:
        base.print_washers(game_state)

    cube.prin_cube(game_state.screen, game_state.cubs_was_trow)
    pygame.display.update()


def main_game_loop(game_state):
    dec, cube, skip_butt, was_move = initialize_game(game_state)

    running = True
    while running:
        result = handle_events(game_state, cube)
        if result is not None:
            return result

        game_over_result = check_game_over(game_state)
        if game_over_result is not None:
            return game_over_result

        was_move = update_game_state(game_state, was_move)
        render_game(game_state, dec, skip_butt, cube)
        game_state.clock.tick(60)
    return "None"