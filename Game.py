import math
from Cube import *


class GameState:
    def __init__(self):
        self.move_is_going = False
        self.move_color = "Black"
        self.baseList = []
        self.cubes_num = [1, 1]
        self.move_index = 0
        self.cubs_was_trow = False
        self.count_of_black = 0
        self.count_of_white = 0
        self.screen = None
        self.clock = None


def change_move(game_state):
    game_state.move_index = 0
    game_state.cubs_was_trow = False
    if game_state.move_color == "Black":
        game_state.move_color = "White"
    else:
        game_state.move_color = "Black"


class SkipButton:
    def __init__(self):
        self.small_image = pygame.transform.scale(pygame.image.load("Images/кнопкаSkip.png"), (40, 30))
        self.big_image = pygame.transform.scale(pygame.image.load("Images/кнопкаSkip.png"), (57, 45))
        self.image = self.small_image
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.state = "Small"

    def check_mouse(self, game_state):
        self.image = self.small_image
        self.state = "Small"
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and self.state == "Small" and not game_state.move_is_going:
            self.image = self.big_image
            self.state = "Big"
        if self.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] and game_state.cubs_was_trow:
            change_move(game_state)
        self.print_button(game_state)

    def print_button(self, game_state):
        game_state.screen.blit(self.image, (0, 0))


def remove_from_game(game_state, washer: 'Washer'):
    washer.base.pop_washer()
    if game_state.move_color == "Black":
        game_state.count_of_black += 1
    else:
        game_state.count_of_white += 1
    game_state.move_index += 1
    if game_state.move_index == 2:
        change_move(game_state)


def can_move(game_state, washer, count, index_of_base):
    if not _check_basic_conditions(game_state, washer):
        return False

    if not _check_board_bounds(game_state, washer, count, index_of_base):
        return False

    return _check_target_base(game_state, washer, count, index_of_base)


def _check_basic_conditions(game_state, washer):
    if not _check_player_home(game_state, washer):
        return False

    if game_state.move_is_going:
        return False

    if washer.index + 1 != washer.base.count:
        return False

    return True


def _check_player_home(game_state, washer):
    if washer.color == "Black":
        save_base = game_state.baseList[0]
    else:
        save_base = game_state.baseList[25]

    if save_base.count > 0:
        return washer.base.num == save_base.num

    return True


def _check_board_bounds(game_state, washer, count, index_of_base):
    target_position = index_of_base + count

    if 1 > target_position or target_position > 24:
        remove_from_game(game_state, washer)
        return False

    return True


def _check_target_base(game_state, washer, count, index_of_base):
    target_position = index_of_base + count
    next_base = game_state.baseList[target_position]

    if next_base.count == 0 or next_base.washers[0].color == washer.color:
        return True

    if next_base.count == 1 and next_base.washers[0].color != washer.color:
        _knock_opponent_washer(game_state, next_base)
        return True

    if next_base.count > 1 and next_base.washers[0].color != washer.color:
        return False

    return True


def _knock_opponent_washer(game_state, next_base):
    opponent_washer = next_base.washers[0]

    if opponent_washer.color == "Black":
        save_base = game_state.baseList[0]
    else:
        save_base = game_state.baseList[25]

    set_param_for_knocked(game_state, next_base, save_base)


def set_param_for_knocked(game_state, next_base, save_base):
    next_base.washers[0].base = save_base
    next_base.washers[0].x = save_base.x
    next_base.washers[0].y = save_base.y + 50 * save_base.count
    next_base.washers[0].index = save_base.count
    next_base.washers[0].whasher_rect = next_base.washers[0].image.get_rect(
        topleft=(save_base.x, save_base.y + 50 * save_base.count))
    save_base.add_washer(next_base.washers[0])
    next_base.pop_washer()


class Washer:
    normalImage = -1
    bigImage = -1
    size = 33
    direction = 0

    def __init__(self, color_type: str, x: int, y: int, base, index: int):
        self.color = color_type
        self.index = index
        if color_type == "Black":
            self.normalImage = pygame.transform.scale(pygame.image.load("Images/фишкачерная.png"),
                                                      (self.size, self.size))
            self.bigImage = pygame.transform.scale(pygame.image.load("Images/фишкачерная.png"),
                                                   (self.size * 1.1, self.size * 1.1))
            self.direction = 1
        elif color_type == "White":
            self.normalImage = pygame.transform.scale(pygame.image.load("Images/фишкабелая.png"),
                                                      (self.size, self.size))
            self.bigImage = pygame.transform.scale(pygame.image.load("Images/фишкабелая.png"),
                                                   (self.size * 1.1, self.size * 1.1))
            self.direction = -1
        else:
            raise Exception("Неправильно указан цвет")
        self.whasher_rect = self.normalImage.get_rect(topleft=(x, y))
        self.x, self.y = x, y
        self.base = base
        self.image = self.normalImage
        self.nextBase = base

    whasher_rect = -1
    state = "Small"
    base = -1
    index = -1
    nextBase = -1

    def check_mouse_on_washer(self, game_state):
        self.image = self.normalImage
        self.state = "Small"
        if not game_state.cubs_was_trow:
            return

        mouse = pygame.mouse.get_pos()
        if self.whasher_rect.collidepoint(mouse) and self.state == "Small" and not game_state.move_is_going:
            self.image = self.bigImage
            self.state = "Big"

        if not game_state.move_is_going and self.whasher_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            if can_move(game_state, self, game_state.cubes_num[game_state.move_index] * self.direction, self.base.num):
                self.nextBase = game_state.baseList[(self.base.num
                                                     + game_state.cubes_num[game_state.move_index] * self.direction)]
                game_state.move_is_going = True
                self.change_base(self.nextBase)
                self.whasher_is_going = True
        if self.whasher_is_going:
            if self.nextBase.der == 'Down':
                self.move_to(game_state, self.nextBase.x, self.base.y + (self.nextBase.count - 1) * 50)
            else:
                self.move_to(game_state, self.nextBase.x, self.base.y - (self.nextBase.count - 1) * 50)

    def change_base(self, new_base):
        self.base.washers.pop(-1)
        self.base.count -= 1
        self.index = len(new_base.washers)
        self.base = new_base
        self.base.add_washer(self)

    def print_washer(self, game_state):
        if game_state.move_color == self.color:
            self.check_mouse_on_washer(game_state)
        game_state.screen.blit(self.image, (self.x, self.y))

    whasher_is_going = False

    def move_to(self, game_state, next_x, next_y):
        delta_x = next_x - self.x
        delta_y = next_y - self.y
        length = math.sqrt(delta_x ** 2 + delta_y ** 2) / 5
        if length / 2 == 0:
            print(game_state.cubes_num[game_state.move_index])
            raise Exception("0")
        delta_x /= length
        delta_y /= length
        self.x, self.y = self.x + delta_x, self.y + delta_y
        if length < 1:
            self.x, self.y = next_x, next_y
        self.whasher_rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.x == next_x and self.y == next_y:
            game_state.move_is_going = False
            self.whasher_is_going = False


class Base:
    x = 0
    y = 0
    count = 0

    def __init__(self, game_state, x, y, num, der):
        self.num = num
        self.der = der
        game_state.baseList.append(self)
        self.baseList = game_state.baseList
        self.x, self.y = x, y
        self.washers = []

    def print_washers(self, game_state):
        for washer in self.washers:
            washer.print_washer(game_state)

    def add_washer(self, washer):
        self.washers.append(washer)
        self.count += 1

    def pop_washer(self):
        self.washers.pop(-1)
        self.count -= 1