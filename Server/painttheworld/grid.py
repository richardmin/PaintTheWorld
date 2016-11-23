# painttheworld/game.py
#
# Represent and track the current game state.

import numpy as np
import datetime
import math
from painttheworld import const
from painttheworld.coord import haversine

class OutOfBoundsException(Exception):
    pass

''' Note that Latitude is North/South and Longitude is West/East'''
class Grid:
    """Keeps track of which teams have colored which areas of the map.

    The map is a grid that's represented by a 2D array containing values
    corresponding to which team controls that area/block of the map.  Clients
    perform the necessary GPS -> grid coordinate calculations and send their
    game state updates in grid coordinates via the update() method.

    TODO: might have to add coordinate transformations to our methods since
          (0,0) is technically the center of our grid.
    """

    def __init__(self):
        """Create a GameState object."""
        size = 2 * const.RADIUS + 1
        self.array = np.zeros((size, size), dtype=np.int8)

    def update_grid(self, coord, team):
        if inside_grid(coord):
            self.array[coord]

    def inside_grid(self, grid_coord):
        lowest_coord = (0,0)
        highest_coord = (const.RADIUS*2 + 1, const.RADIUS*2 + 1)
        lower_bound = np.all(np.greater_equal(grid_coord, lowest_coord))
        upper_bound = np.all(np.less_equal(grid_coord, highest_coord))
        return lower_bound and upper_bound
         
    @staticmethod
    def diff(a, b):
        """Calculate the deltas of two Grid objects.
        Args:
            a (Grid) - the "older" Grid object
            b (Grid): the "updated" Grid object

        Returns:
            List of coordinate/team pairings of the form ((x,y), team_color).
        """
        diff = np.absolute(a.array - b.array)
        coord = np.nonzero(diff)
        val = diff[coord]
        coord = map(tuple, np.transpose(coord))  # turn coord into (x,y) tuples
        return list(zip(coord, val))
