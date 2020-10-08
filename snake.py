import sys
import pygame
from random import randint

# some global settings
nrow = 10
width = 50


def draw_grid(width, nrow, surface):
    """creates chessgrid for surface"""
    s_width = width * nrow
    col = (255, 255, 255)
    for l in range(nrow):
        pygame.draw.line(surface, col, (l * width, 0), (l * width, s_width))
        pygame.draw.line(surface, col, (0, l * width), (s_width, l * width))


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = randint(0, nrow-1)
        self.y = randint(0, nrow-1)
        # self.image = pygame.Surface([width, width])
        # self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x_dir = 0
        self.y_dir = 1
        # self.image = pygame.Surface([width, width])
        # self.image.fill((0,225, 0))
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)
        self.tail = [] # elem should be a list of rect

    def draw(self, surface):
        """prints whole snake on surface"""
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        #print("---------------------------")
        #print(self.rect)
        for rect in self.tail:
            pygame.draw.rect(surface, (0, 0, 255), rect)
        #print(self.tail)
        #print("---------------------------")

    def move_head(self):
        """updates new position of head, given keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_dir = -1
                    self.y_dir = 0
                elif event.key == pygame.K_RIGHT:
                    self.x_dir = 1
                    self.y_dir = 0
                elif event.key == pygame.K_UP:
                    self.x_dir = 0
                    self.y_dir = -1
                elif event.key == pygame.K_DOWN:
                    self.x_dir = 0
                    self.y_dir = 1

        self.x = (self.x_dir + self.x) % nrow  # ensure the world wraps around
        self.y = (self.y_dir + self.y) % nrow
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)


    def move_tail(self, eating = False):
        """updates new position of tail"""
        if eating == True:
            new_tail = [self.rect] + self.tail
        #    print(new_tail)
            self.tail = new_tail
        #    print('OMG')
        else:
            new_tail = [self.rect] + self.tail
            self.tail = new_tail[:-1]


    def eat(self, apple):
        return pygame.sprite.collide_rect(self, apple)


    def move_snake(self, apple):
        """updates new snake pos"""
        eating = Snake.eat(self, apple)
        self.move_tail(eating = eating)
        self.move_head()





def main():
    # Initialise screen
    s_width = nrow*width
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_width))
    pygame.display.set_caption('Basic Snake')

    # Make background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    draw_grid(width, nrow, background)

    # Make apple 
    apple = Apple()

    # Make snake
    snake = Snake(8,1)
    #snake.tail = [pygame.Rect(snake.x * width, (snake.y+1) * width, width, width),
    #                pygame.Rect(snake.x * width, (snake.y+2) * width, width, width)]
    #snake.tail = []
    # Initialise clock
    clock = pygame.time.Clock()

    while 1:
        clock.tick(1)
        screen.blit(background, (0,0))
        apple.draw(screen)
        snake.move_snake(apple)
        snake.draw(screen)
        snake.eat(apple)


        pygame.display.flip()









if __name__  == '__main__': main()