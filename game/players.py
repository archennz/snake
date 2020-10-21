import pygame
import os
from game.world import nrow, width
from random import randint


class Apple():
    def get_image(image_name):
        try:
            full_name = os.path.join('images', image_name)
            image = pygame.image.load(full_name)
        except pygame.error as message:
            print('Cannot load image', image_name)
            raise SystemExit(message)
        image = image.convert()
        image = pygame.transform.scale(image, (width, width))
        colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
        return image

    def __init__(self):
        """ Apples comes with randomly generated inherent x,y position"""
        self.x = randint(0, nrow-1)
        self.y = randint(0, nrow-1)
        self.image = Apple.get_image('apple.png')

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
        #pygame.sprite.Sprite.__init__(self)
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
        pygame.draw.circle(surface, (0, 255, 0), cent,rad)
        for rect in self.tail:
            pygame.draw.rect(surface, (0, 0, 255), rect)

    def move_head(self):
        """update position according to direction """
        self.x = (self.x_dir + self.x) % nrow  # ensure the world wraps around
        self.y = (self.y_dir + self.y) % nrow
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def receive_orders(self, orders):
        """ Given orders 'L' 'R' 'U' 'D',
            updates direction of snake head in the next frame """
        if orders == 'L':
            self.x_dir = -1
            self.y_dir = 0
        if orders == 'R':
            self.x_dir = 1
            self.y_dir = 0
        elif orders == 'U':
            self.x_dir = 0  # remember things are upside down in pygame
            self.y_dir = -1
        elif orders == 'D':
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
