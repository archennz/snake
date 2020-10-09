import pygame
from world import nrow, width  # import size of world
from players import Apple, Snake


def draw_grid(width, nrow, surface):
    """creates chessgrid for surface"""
    s_width = width * nrow
    col = (255, 255, 255)
    for l in range(nrow):
        pygame.draw.line(surface, col, (l * width, 0), (l * width, s_width))
        pygame.draw.line(surface, col, (0, l * width), (s_width, l * width))


def initialise_screen(nrow, width):
    """makes screen and draw grid
        returns screen and background as objects"""
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
    forbidden = snake.get_pos()
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


def print_score(score, screen):
    font = pygame.font.Font(None, 36)
    message = "You lost, your score is " + str(score)
    box = font.render(message, 1, (219, 117, 49))
    textpos = box.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(box, textpos)
    pygame.display.flip()


def main():

    screen, background = initialise_screen(nrow, width)

    # Make snake
    snake = Snake(8, 1)
    # Make apple
    apple = initialise_apple(snake)

    # Initialise clock
    clock = pygame.time.Clock()

    score = 0

    # it checks for the tangle a little bit too late for length 2 snake
    while not snake.is_tangled():
        clock.tick(1)
        screen.blit(background, (0, 0))

        # draws apple
        apple.draw(screen)

        eaten = is_eating(snake, apple)

        # checks if snake touching apple and update next 
        snake.move_snake(get_control(), eating = eaten)

        if eaten:
            score += 1
            forbidden = snake.get_pos()
            apple.displace(forbidden)

        # draws snake and tail
        snake.draw(screen)

        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        print_score(score, screen)





if __name__  == '__main__': main()