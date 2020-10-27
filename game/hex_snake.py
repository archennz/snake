import pygame
from game.world import nrow, width
from players import HexApple, HexSnake
from utils import initialise_screen, move_apple, is_eating, print_score
import hex_utils


def draw_grid(width, nrow, surface):
    """ creates hexagons for surface"""
    for i in range(nrow):
        for j in range(nrow):
            game_coord = hex_utils.change_coord((i, j))
            points = hex_utils.make_hex_points(game_coord, width/2)
            col = (255, 255, 255)
            pygame.draw.lines(surface, col, True, points)


def get_control():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                return 'L'
            elif event.key == pygame.K_d:
                return 'R'
            elif event.key == pygame.K_w:
                return 'UL'
            elif event.key == pygame.K_e:
                return 'UR'
            elif event.key == pygame.K_z:
                return 'DL'
            elif event.key == pygame.K_x:
                return 'DR'


def main():
    # make world
    # the initialise_screen method is a bit weird
    s_length = width*(nrow+1)*3/4
    s_width = hex_utils.get_cross_width(width)*(nrow + 1)
    screen, background = initialise_screen(s_width, s_length, "Hex Snake")
    draw_grid(width, nrow, background)
    clock = pygame.time.Clock()
    score = 0

    # Make characters
    snake = HexSnake(8, 1)
    apple = move_apple(HexApple(), snake)

    # it checks for the tangle a little bit too late for length 2 snake
    while not snake.is_tangled():
        clock.tick(1)
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


if __name__ == '__main__':
    main()
