import pygame
from players import Apple

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