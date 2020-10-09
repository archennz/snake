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
        """ Apples comes with randomly generated inherent x,y position"""
        pygame.sprite.Sprite.__init__(self)
        self.x = randint(0, nrow-1)
        self.y = randint(0, nrow-1)
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def displace(self, forbidden):
        """Given a list of forbidden coordinates, moves apple to avilable new coordinates"""
        while (self.x, self.y) in forbidden:
            self.x = randint(0, nrow-1)
            self.y = randint(0, nrow-1)
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Given x,y position, assign snake of length 1"""
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x_dir = 0
        self.y_dir = 1
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)
        self.tail = []  # elem should be a list of rect objects
        self.tail_pos = []  # elem should be a list of coord (x,y)

    def draw(self, surface):
        """prints snake head and tail on surface"""
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        for rect in self.tail:
            pygame.draw.rect(surface, (0, 0, 255), rect)

    def move_head(self, orders):
        """ Given orders 'L' 'R' 'U' 'D', 
            updates position of snake head in the next frame
            continue with existing direction if received no orders """
        if orders == 'L':
            self.x_dir = -1
            self.y_dir = 0
        if orders == 'R':
            self.x_dir = 1
            self.y_dir = 0
        elif orders == 'U':
            self.x_dir = 0
            self.y_dir = -1
        elif orders == 'D':
            self.x_dir = 0
            self.y_dir = 1

        self.x = (self.x_dir + self.x) % nrow  # ensure the world wraps around
        self.y = (self.y_dir + self.y) % nrow
        self.rect = pygame.Rect(self.x * width, self.y * width, width, width)

    def move_tail(self, eating = False):
        """updates new position of tail
            grows tail by one if eating"""
        new_tail = [self.rect] + self.tail
        new_tail_pos = [(self.x, self.y)] + self.tail_pos
        if eating == True:
            self.tail = new_tail
            self.tail_pos = new_tail_pos
        else:
            self.tail = new_tail[:-1]
            self.tail_pos = new_tail_pos[:-1]

    def is_tangled(self):
        """ returns False if snake is moving into itself"""
        return (self.x, self.y) in self.tail_pos

    def move_snake(self, orders, eating = False):
        """ update whole snake position depending if snake is eating
            disallows illegal snake moves"""
        if self.is_tangled():
            print("fucked up") # should probably fix this to print something better
            pygame.quit()
        else:
            self.move_tail(eating = eating)
            self.move_head(orders)


    def eat(self, apple):
        return pygame.sprite.collide_rect(self, apple)



def initialise_screen(nrow, width):
    """makes screen and draw grid"""    
    s_width = nrow*width
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_width))
    pygame.display.set_caption('Basic Snake')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    draw_grid(width, nrow, background)

    return screen, background


def initialise_apple(snake):
    """ given snake, makes apple not overlapping snake """
    apple = Apple()
    forbidden = [(snake.x, snake.y)] + snake.tail_pos
    apple.displace(forbidden)
    return apple

def is_eating(snake, apple):
    """ check if snake head is in same pos as apple """
    return (snake.x, snake.y) == (apple.x, apple.y)

def get_control():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return 'L'
            elif event.key == pygame.K_RIGHT:
                return 'R'
            elif event.key == pygame.K_UP:
                return 'U'
            elif event.key == pygame.K_DOWN:
                return 'D'

def main():

    screen, background = initialise_screen(nrow, width)

    # Make snake
    snake = Snake(8,1)

    # Make apple
    apple = initialise_apple(snake)

    # Initialise clock
    clock = pygame.time.Clock()

    while 1:
        clock.tick(1)
        screen.blit(background, (0,0))

        # draws apple
        apple.draw(screen)

        eaten = is_eating(snake, apple)

        # checks if snake touching apple and update next 
        snake.move_snake(get_control(), eating = eaten)

        if eaten:
            forbidden = [(snake.x, snake.y)] + snake.tail_pos
            apple.displace(forbidden)

        # draws snake and tail
        snake.draw(screen)

        # if snake.eat(apple):
        #   
        #    apple.displace(forbidden)



        pygame.display.flip()









if __name__  == '__main__': main()