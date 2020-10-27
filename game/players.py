import pygame
import os
from game.world import nrow, width
from random import randint
from game.hex_utils import convert_coord_to_game_coord, make_hex_points_from_coord


class Apple():
    def __init__(self):
        """ Apples comes with randomly generated inherent x,y position"""
        self.x = randint(0, nrow-1)
        self.y = randint(0, nrow-1)
        self.image = Apple.get_image('apple.png', width)

    @staticmethod
    def get_image(image_name, width):
        try:
            full_name = os.path.join('game/images', image_name)
            image = pygame.image.load(full_name)
        except pygame.error as message:
            print('Cannot load image', image_name)
            raise SystemExit(message)
        # image = image.convert()
        image = pygame.transform.scale(image, (width, width))
        colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
        return image

    def displace(self, forbidden):
        """Given list of forbidden coord, moves apple to avilable new coord"""
        while (self.x, self.y) in forbidden:
            self.x = randint(0, nrow-1)
            self.y = randint(0, nrow-1)

    def draw(self, surface):
        surface.blit(self.image, (self.x * width, self.y * width))


class Snake():
    def __init__(self, x, y):
        """ Given x,y position, assign snake of length 1"""
        self.x = x
        self.y = y
        self.x_dir = 0
        self.y_dir = 1
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)
        self.tail = []  # elem should be a list of rect objects
        self.tail_pos = []  # elem should be a list of coord (x,y)

    def draw(self, surface):
        """prints snake head and tail on surface"""
        rad = width/2
        cent = (self.x * width + rad, self.y * width + rad)
        pygame.draw.circle(surface, (0, 255, 0), cent, rad)
        for rect in self.tail:
            pygame.draw.rect(surface, (0, 0, 255), rect)

    def move_head(self):
        """update position according to direction """
        self.x = (self.x_dir + self.x) % nrow  # ensure the world wraps around
        self.y = (self.y_dir + self.y) % nrow
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def receive_orders(self, order):
        """ Given orders 'L' 'R' 'U' 'D',
            updates direction of snake head in the next frame """
        if order == 'L':
            self.x_dir = -1
            self.y_dir = 0
        if order == 'R':
            self.x_dir = 1
            self.y_dir = 0
        elif order == 'U':
            self.x_dir = 0  # remember things are upside down in pygame
            self.y_dir = -1
        elif order == 'D':
            self.x_dir = 0
            self.y_dir = 1

    def move_tail(self, eating=False):
        """updates new position of tail
            grows tail by one if eating"""
        new_tail = [self.rect] + self.tail
        new_tail_pos = [(self.x, self.y)] + self.tail_pos
        if eating is True:
            self.tail = new_tail
            self.tail_pos = new_tail_pos
        else:
            self.tail = new_tail[:-1]
            self.tail_pos = new_tail_pos[:-1]

    def is_tangled(self):
        """ returns False if snake is moving into itself"""
        return (self.x, self.y) in self.tail_pos

    def move_snake(self, orders, eating=False):
        """ update whole snake position depending if snake is eating"""
        self.move_tail(eating=eating)
        self.receive_orders(orders)
        self.move_head()

    def get_pos(self):
        """ gives list of position of head and tail"""
        return [(self.x, self.y)] + self.tail_pos


class HexSnake(Snake):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direc = 'DR'

    def draw_mouth(self, surface):
        """draw solid triangle where the mouth is"""
        inner_rad = width/2
        head_hex = make_hex_points_from_coord((self.x, self.y), inner_rad)
        head_center = convert_coord_to_game_coord((self.x, self.y))
        mouth_col = (0, 0, 0)
        if self.direc == 'R':
            mouth = head_hex[0:2] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)
        elif self.direc == 'DR':
            mouth = head_hex[1:3] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)
        elif self.direc == 'DL':
            mouth = head_hex[2:4] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)
            pygame.draw.polygon(surface, mouth_col, mouth)
        elif self.direc == 'L':
            mouth = head_hex[3:5] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)
        elif self.direc == 'UL':
            mouth = head_hex[4:] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)
        elif self.direc == 'UR':
            mouth = [head_hex[5]] + [head_hex[0]] + [head_center]
            pygame.draw.polygon(surface, mouth_col, mouth)

        

    def draw(self, surface):
        inner_rad = width/2
        head_col = (0, 255, 0)
        tail_col = (19, 161, 97)
        head_hex = make_hex_points_from_coord((self.x, self.y), inner_rad)
        pygame.draw.polygon(surface, head_col, head_hex)
        self.draw_mouth(surface)
        for tail_piece in self.tail_pos:
            tail_hex = make_hex_points_from_coord((tail_piece), inner_rad)
            pygame.draw.polygon(surface, tail_col, tail_hex)

    def receive_orders(self, order):
        """ Given orders 'L' 'R' 'UL' 'UR' 'DL' 'DR',
            updates direction of snake head in the next frame """
        if order == 'L':
            self.direc = order
            self.x_dir = -1
            self.y_dir = 0
        if order == 'R':
            self.direc = order
            self.x_dir = 1
            self.y_dir = 0
        elif order == 'DL':
            self.direc = order
            self.x_dir = -1  # remember things are upside down in pygame
            self.y_dir = 1
        elif order == 'DR':
            self.direc = order
            self.x_dir = 0  # remember things are upside down in pygame
            self.y_dir = 1
        elif order == 'UL':
            self.direc = order
            self.x_dir = 0
            self.y_dir = -1
        elif order == 'UR':
            self.direc = order
            self.x_dir = 1
            self.y_dir = -1


class HexApple(Apple):
    def __init__(self):
        super().__init__()
        self.image = Apple.get_image('apple.png', width//2)

    def draw(self, surface):
        coord = (self.x, self.y)
        (center_x, center_y) = convert_coord_to_game_coord(coord)
        game_cart_coord = (center_x - width//4, center_y - width//4)
        surface.blit(self.image, game_cart_coord)
