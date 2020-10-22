import pygame
from game.world import nrow, width  # import size of world
from players import Apple, Snake

def initialise_screen(nrow, width):
    """makes screen
        returns screen and background as objects"""
    s_width = nrow*width
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_width))
    pygame.display.set_caption('Basic Snake')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    return screen, background


def move_apple(apple, snake):
    """ given snake, makes apple not overlapping snake """
    # apple = Apple()
    forbidden = snake.get_pos()
    apple.displace(forbidden)
    return apple


def is_eating(snake, apple):
    """ check if snake head is in same pos as apple """
    return (snake.x, snake.y) == (apple.x, apple.y)


def print_score(score, screen):
    font = pygame.font.Font(None, 36)
    message = "You lost, your score is " + str(score)
    box = font.render(message, 1, (219, 117, 49))
    textpos = box.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(box, textpos)
    pygame.display.flip()
