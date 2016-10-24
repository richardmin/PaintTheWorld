# painttheworld/game.py
#
# Represent and track the current game state.

import msgpack as mp
import numpy as np

# Teams
NONE = 0
RED = 1
BLUE = 2

class GameState:
    """Keeps track of which teams have colored which areas of the map.

    The map is a grid that's represented by a 2D array containing values
    corresponding to which team controls that area/block of the map.  Clients
    perform the necessary GPS -> grid coordinate calculations and send their
    game state updates in grid coordinates via the update() method.

    TODO: might have to add coordinate transformations to our methods since
          (0,0) is technically the center of our grid.
    """

    def __init__(self, radius):
        """Create a GameState object.

        Args:
            radius: the number of grid blocks from the center block in the
                    vertical/horizontal direction.
        """
        size = 2*radius + 1
        self.grid = np.zeros((size, size), dtype=np.int8)
        self.radius = radius

    def update(self, coord, team):
        """Update the game state array."""
        x, y = coord
        self.grid[x][y] = team

    @staticmethod
    def diff(a, b):
        """Calculate the deltas of two GameState objects.

        Returns:
            List of coordinate/team pairings of the form ((x,y), team_color).
        """
        diff = a.grid - b.grid
        coord = np.nonzero(diff)
        val = diff[coord]
        coord = map(tuple, np.transpose(coord))  # turn coord into (x,y) tuples
        return list(zip(coord, val))
