import pygame
from game.world import nrow, width
from players import Apple, Snake
from utils import *

def draw_grid(width, nrow, surface):
    """creates chessgrid for surface"""
    s_width = width * nrow
    col = (255, 255, 255)
    for l in range(nrow):
        pygame.draw.line(surface, col, (l * width, 0), (l * width, s_width))
        pygame.draw.line(surface, col, (0, l * width), (s_width, l * width))

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
    # make world
    s_width = nrow*width
    screen, background = initialise_screen(s_width, s_width, "Rect Snake")
    draw_grid(width, nrow, background)
    clock = pygame.time.Clock()
    score = 0

    # Make characters
    snake = Snake(8, 1)
    apple = move_apple(Apple(), snake)

    # it checks for the tangle a little bit too late for length 2 snake
    while not snake.is_tangled():
        clock.tick(3)
        screen.blit(background, (0, 0))
        apple.draw(screen)
        snake.draw(screen)

        eaten = is_eating(snake, apple)
        # checks if snake touching apple and update next
        snake.move_snake(get_control(), eating=eaten)
        if eaten:
            score += 1
            move_apple(apple, snake)

        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        print_score(score, screen)


if __name__ == '__main__' :main()
