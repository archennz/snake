import pygame
from game.world import nrow, width
from players import Apple, Snake
from utils import *

def main():
    # make world
    screen, background = initialise_screen(nrow, width)
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
