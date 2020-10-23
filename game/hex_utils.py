from game.world import nrow, width
from math import cos, sin, radians
import matplotlib.pyplot as plt


def change_coord(coord):
    """change coord from (column, row) to game coord
    game coord change big row numbers to negative
    for wrapping around"""
    (column, row) = coord
    offset = row//2
    if column >= (nrow - offset):
        n = column - nrow
        return (n, row)
    return (column, row)


def draw_game_coord(game_coord):
    """render game coord into cartesian coord for pygame surface"""
    (column, row) = game_coord
    cross_width = cos(radians(30))*width
    game_x = cross_width/2 + row*cross_width/2 + column*cross_width
    game_y = width/2 + row*cross_width*cos(radians(30))
    return (game_x, game_y)


def convert_coord_to_game_coord(coord):
    """change coord from (column, row) to cartesian coord for pygame"""
    game_coord = change_coord(coord)
    return draw_game_coord(game_coord)


def make_hex(cart_coord, inner_rad):
    """given cartesian coord of center, return cartesian coord for
    six points of hexagon"""
    points = []
    (game_x, game_y) = cart_coord
    for i in range(-30, 330, 60):
        new_x = game_x + inner_rad*cos(radians(i))
        new_y = game_y + inner_rad*sin(radians(i))
        points.append((new_x, new_y))
    return points


def make_hex_points(game_coord, inner_rad):
    """given game coord, returns cartesion coord for
    the six pts on the hex surrounding center"""
    cart_coord = draw_game_coord(game_coord)
    return make_hex(cart_coord, inner_rad)

def make_hex_points_from_coord(coord, inner_rad):
    """given (row, column) return cartesian coord for 
    the six points on the hex surrounding center"""
    game_coord = change_coord(coord)
    return make_hex_points(game_coord, inner_rad)


def draw_game_center():
    """debugging by drawing the centers of each hexagon
    in the game world"""
    xs = []
    ys = []
    for i in range(nrow):
        for j in range(nrow):
            game_coord = change_coord((i, j))
            (plot_x, plot_y) = draw_game_coord(game_coord)
            xs.append(plot_x)
            ys.append(plot_y)
    plt.scatter(xs, ys)
    plt.show()


def draw_game_hex():
    """debugging by drawing the centers and hex edges
    in the game world"""
    inner_rad = width*(1/3)
    xs = []
    xs_pts = []
    ys = []
    ys_pts = []
    for i in range(nrow):
        for j in range(nrow):
            game_coord = change_coord((i, j))
            (plot_x, plot_y) = draw_game_coord(game_coord)
            points = make_hex_points(game_coord, inner_rad)
            for (x, y) in points:
                xs_pts.append(x)
                ys_pts.append(y)
            xs.append(plot_x)
            ys.append(plot_y)
    plt.scatter(xs, ys)
    plt.scatter(xs_pts, ys_pts, marker='*')
    plt.show()


if __name__ == '__main__': draw_game_hex()
