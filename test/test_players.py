from game import players
from game.world import nrow


class TestApple:
    def test_apple_inside_world(self):
        apple = players.Apple()
        assert apple.x in range(0, nrow)
        assert apple.y in range(0, nrow)

    def test_apple_properly_displaced_horizontal(self):
        for i in range(0, nrow):
            apple = players.Apple()
            forbidden = [(x, i) for x in range(0, nrow)]
            apple.displace(forbidden)
            assert apple.y != i

    def test_apple_properly_displaced_vertical(self):
        for i in range(0, nrow):
            apple = players.Apple()
            forbidden = [(i, y) for y in range(0, nrow)]
            apple.displace(forbidden)
            assert apple.x != i


class TestSnake:
    def test_snake_move_head(self):
        if nrow >= 1:
            snake = players.Snake(0, 0)
            snake.move_head()
            assert (snake.x, snake.y) == (0, 1)

    def test_receive_orders_down(self):
        snake = players.Snake(0, 0)
        snake.receive_orders('D')
        snake.move_head()
        assert (snake.x, snake.y) == (0, 1)

    def test_receive_orders_up(self):
        snake = players.Snake(0, nrow-1)
        snake.receive_orders('U')
        snake.move_head()
        assert (snake.x, snake.y) == (0, nrow-2)

    def test_receive_orders_left(self):
        snake = players.Snake(nrow-1, 0)
        snake.receive_orders('L')
        snake.move_head()
        assert (snake.x, snake.y) == (nrow-2, 0)

    def test_receive_orders_right(self):
        snake = players.Snake(0, 0)
        snake.receive_orders('R')
        snake.move_head()
        assert (snake.x, snake.y) == (1, 0)

    def test_move_world_wraps_around_up_down(self):
        snake = players.Snake(0, 0)
        snake.receive_orders('U')
        snake.move_head()
        assert (snake.x, snake.y) == (0, nrow-1)
        snake.receive_orders('D')
        snake.move_head()
        assert (snake.x, snake.y) == (0, 0)

    def test_move_world_wraps_around_left_right(self):
        snake = players.Snake(0, 0)
        snake.receive_orders('L')
        snake.move_head()
        assert (snake.x, snake.y) == (nrow-1, 0)
        snake.receive_orders('R')
        snake.move_head()
        assert (snake.x, snake.y) == (0, 0)

    def test_move_tail(self):
        pass

    def test_is_tangled(self):
        pass

    def test_get_pos(self):
        pass

    def test_move_snake(self):
        pass
