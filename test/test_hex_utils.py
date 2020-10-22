from game import hex_utils
from game.world import nrow
import pytest


class TestChangeCoord:
    # need a minimum bound on nrow
    @pytest.mark.parametrize('x_coord, game_coord', [
        # first row
        ((0, 0), (0, 0)),
        ((1, 0), (1, 0)),
        ((nrow-1, 0), (nrow-1, 0)),
        ((nrow-2, 0), (nrow-2, 0)),
        # second row
        ((0, 1), (0, 1)),
        ((1, 1), (1, 1)),
        ((nrow-1, 1), (nrow-1, 1)),
        ((nrow-2, 1), (nrow-2, 1)),
        # third row
        ((0, 2), (0, 2)),
        ((1, 2), (1, 2)),
        ((nrow-1, 2), (-1, 2)),
        ((nrow-2, 2), (nrow-2, 2)),
        # fourth row
        ((0, 3), (0, 3)),
        ((1, 3), (1, 3)),
        ((nrow-1, 3), (-1, 3)),
        ((nrow-2, 3), (nrow-2, 3))
    ])
    def test_change_coord(self, x_coord, game_coord):
        assert hex_snake.change_coord(x_coord) == game_coord


# the next couples of functions should be tested by the pyplot debugger
# draw_game_center
# draw_game_coord
