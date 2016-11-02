# painttheworld/game.py
#
# Represent and track the current game state.

import numpy as np
from math import radians, cos, sin, asin, sqrt

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

    def __init__(self, radius, coords):
        """Create a GameState object.

        Args:
            radius: the number of grid blocks from the center block in the
                    vertical/horizontal direction.

            coords: a list of the 8 user locations (made when creating the lobby)
                    The user locations should be tuples in the format x, y
        """
        size = 2*radius + 1
        self.grid = np.zeros((size, size), dtype=np.int8)
        self.radius = radius
        length = len(coords)
        self.center_coord = (sum(i for i, _ in coords)/length, sum(i for _, i in coords)/length
        self.longitude_conversion = calculateLongitudeToMiles(center_coord)

    def update(self, coord, team):
        """Update the game state array."""
        x, y = coord
        self.grid[x][y] = team

    def convert(self, coord)
        """ Casts a GPS coordinate onto the grid, predefined by center_coord
        """
        lon, lat = coord

    @staticmethod
    def diff(a, b):
        """Calculate the deltas of two GameState objects.

        Returns:
            List of coordinate/team pairings of the form ((x,y), team_color).
        """
        diff = np.absolute(a.grid - b.grid)
        coord = np.nonzero(diff)
        val = diff[coord]
        coord = map(tuple, np.transpose(coord))  # turn coord into (x,y) tuples
        return list(zip(coord, val))

    @staticmethod
    def calculateLongitudeToMiles(coord):
        """Calculates the conversion rate for 1 degree of longitude to miles

        Returns:
            Conversion rate for 1 degree of longitude to miles
        """
        # math.cos()

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        Source code from: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km
