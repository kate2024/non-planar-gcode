
"""
This program is to be used for 3D printing.
Uses arrays to assign directions to each cell in a grid.
The 3D printer will print in a straight line in the direction of the cell,
then move to the next cell in the direction of the cell.
It will continue to print until it reaches the end of the grid.
The 3D printer will then move to the next row and repeat the process,
and continue to print until it reaches the end of the grid.
"""

import numpy as np


UP = 1
UP_RIGHT = 2
RIGHT = 3
DOWN_RIGHT = 4
DOWN = 5
DOWN_LEFT = 6
LEFT = 7
UP_LEFT = 8
DONE = 9

DIRECTIONS = {
    UP: (-1, 0),
    UP_RIGHT: (-1, 1),
    RIGHT: (0, 1),
    DOWN_RIGHT: (1, 1),
    DOWN: (1, 0),
    DOWN_LEFT: (1, -1),
    LEFT: (0, -1),
    UP_LEFT: (-1, -1),
}


def main():
    """Main function."""
    width = 6
    height = 5
    directions = assign_directions(width, height)
    fill_grid(directions)
    print(directions)
    print_gcode(directions)


def assign_directions(width, height):
    """Assigns directions to each cell in the grid, diagonals included."""
    directions = np.zeros((height, width))
    return directions


def fill_grid(direction):
    """
    Fills the grid with the correct directions, starting at top left corner.

    Starts with DOWN.
    Loop UP_RIGHT, RIGHT, DOWN_LEFT, DOWN for 'first half' of grid.
    Loop UP_RIGHT, DOWN, DOWN_LEFT, RIGHT for 'second half' of grid.

    If height is even, move UP_RIGHT at bottom left corner; if odd, move RIGHT.
    If width is even, move DOWN at top right corner; if odd, move DOWN_LEFT.

    DONE is assigned to the bottom right corner.
    """
    # Width is the number of columns, height is the number of rows. Loops until DONE.
    # TODO: Figure out IndexError. Shape mismatch, something with reshaping to work with different dimensions?
    height, width = direction.shape
    direction[0::2, 0] = DOWN
    direction[0, 1::2] = RIGHT
    direction[(width % 2)::2, -1] = DOWN  # if width is odd, start at 1, if even start at 0
    direction[-1, (1 - height % 2)::2] = RIGHT  # if height is odd, start at 0, if even start at 1

    # Directions for when position is at bottom left corner.
    if height % 2 == 0 and direction[-1, 0] == 0:
        direction[-1, 0] = UP_RIGHT
    elif height % 2 == 1 and direction[-1, 0] == 0:
        direction[-1, 0] = RIGHT

    # Directions for when position is at top right corner.
    if width % 2 == 0 and direction[0, -1] == 0:
        direction[0, -1] = DOWN
    elif width % 2 == 1 and direction[0, -1] == 0:
        direction[0, -1] = DOWN_LEFT

    for i in range(1, height, 2):
        # Fill in UP_RIGHT until the border is reached.
        direction[
            np.arange(i, 0, -1),  # rows from i to 0
            np.arange(0, i, +1),  # columns from 0 to i
        ] = UP_RIGHT

        # Fill in DOWN_LEFT until the border is reached.
        if i+1 < height:
            direction[
                np.arange(0, i+1, +1),  # rows from 0 to i+1
                np.arange(i+1, 0, -1),  # columns from i+1 to 0
            ] = DOWN_LEFT

    for i in range(height % 2, width, 2):
        # Fill in UP_RIGHT until the border is reached.
        direction[
            np.arange(height-1, i, -1),  # rows from height-1 to i
            np.arange(i, width-1, +1),  # columns from i to width-1
        ] = UP_RIGHT

        # Fill in DOWN_LEFT until the border is reached.
        direction[
            np.arange(i+1, height-1, +1),  # rows from i+1 to height
            np.arange(width-1, i+1, -1),  # columns from width-1 to i
        ] = DOWN_LEFT

    direction[-1, -1] = DONE


def print_gcode(directions):
    """Uses directions of DOWN, RIGHT, UP_LEFT, and DOWN_RIGHT to create G-code for 3D printing.
    Print G-code instruction for each cell in the grid.
    """
    # TODO: Fix instructions.
    # G-code for every cell in the grid.
    print("G0 X0 Y0 Z0")
    i, j = 0, 0  # i == y == row, j == x == column
    while directions[i][j] != DONE:
        cur_direction = directions[i][j]
        di, dj = DIRECTIONS[cur_direction]
        i += di
        j += dj
        next_direction = directions[i][j]
        if next_direction != cur_direction:
            print("G1 X" + str(j) + " Y" + str(i) + " Z0")


if __name__ == "__main__":
    main()
