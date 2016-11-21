# painttheworld/game.py
#
# Represent and track the current game state.

import numpy as np
import datetime
import math
from painttheworld import const
from painttheworld.const import m1, m2, m3, m4, p1, p2, p3
from painttheworld.coord import haversine, conversion_rates

''' Note that Latitude is North/South and Longitude is West/East'''
class GameState:
    """Keeps track of which teams have colored which areas of the map.

    The map is a grid that's represented by a 2D array containing values
    corresponding to which team controls that area/block of the map.  Clients
    perform the necessary GPS -> grid coordinate calculations and send their
    game state updates in grid coordinates via the update() method.

    TODO: might have to add coordinate transformations to our methods since
          (0,0) is technically the center of our grid.
    """

    def __init__(self, radius, gridsize):
        """Create a GameState object.

        Args:
            radius: the number of grid blocks from the center block in the
                vertical/horizontal direction.

            gridsize: The dimensions of a grid tile, in feet. This should be the
                edge length
        """
        size = 2*radius + 1
        self.grid = np.zeros((size, size), dtype=np.int8)
        self.radius = radius
        self.gridsize = gridsize
        self.user_count = 0
        self.user_coords = []
        self.user_grid = []
        self.user_grid.extend([self.grid for i in range(const.lobby_size)])

    def start_game(self):
        """Initialize the starting position of the grid.

        This calculates the center coordinate by average the longitudes and
        latitudes of all people (this might not work too well, as that's not
        really how nautical miles work). Additionally, it sets the start time to
        be 3 seconds from now.
        """
        self.center_coord = np.mean(self.user_coords, axis=1)
        self.conversion_rates = conversion_rates(self.center_coord)
        self.start_time = (datetime.datetime.now() + datetime.timedelta(seconds=3))

    def update(self, coord, team):
        """Update the game state array."""
        x, y = coord
        self.grid[x][y] = team

    def project(self, lon, lat):
        """ Casts a GPS coordinate onto the grid, which has it's central
        locations defined by center_coord.
        """
        vert = haversine(self.center_coord, (self.center_coord[0], lat)) # longitude is east-west, we ensure that's the sam'
        horiz = haversine(self.center_coord, (lon, self.center_coord[1]))

        """ Vectorizes the latitude. The degree ranges from -90 to 90.
            This latitude conversion doesn't handle poles.
            I'm not sure how to handle you playing the game at the north and south pole.
        """ 
        if lat > self.center_coord[1]:
            vert = -vert

        """ Vectorizes the longitude. The degree ranges from -180 to 180.
            There's three cases: 
                1. They're both in the same hemisphere (east/west)
                2. They cross over the 0 degree line
                3. They cross over the 180 degree line
            
            Case (1):
                Check for case 1 by ensuring that the signs are identical.
                If the longitude of the location is less than the longitude of the cenral
                location, that means that we need to move left in the array. 
                We change the sign to be negative.
            Case (2) + (3):
                There's two cases here, where the signs are differing. 
                To determine which line we're crossing, the absolute value of the difference
                in Longitudes is taken. If the difference >180, 
                that implies that the 180 degree is being crossed. Otherwise, it's the 0 degree line.

            Case (2):
                In case (2), if the longitude of the central point is negative, the distance must be positive.
                If the longitude of the central point is positive, the distance must be negative.
            
            Case (3):
                In case (3), if the longitude of the central point is negative, the distance must be negative.
                If the longitude of the central point is positive, the distance must be positive.

        """
        if np.sign(self.center_coord[0]) == np.sign(lon): # Case 1
            if lon > self.center_coord[0]:
                horiz = -horiz
        if math.fabs(self.center_coord[0] - lon) < 180: # Case 2
            if self.center_coord[0] >= 0:
                horiz = -horiz
        elif self.center_coord[0] < 0: # Case 3
            horiz = -horiz

        horiz = math.floor(horiz * 1000 / const.gridsize)
        vert = math.floor(vert * 1000 / const.gridsize)

        return np.add((self.radius + 1, self.radius + 1), (horiz, vert))

    def add_user(self, lat, lon):
        """ Adds a user and their starting location to the grid.

        Returns the user id number assosciated with that user, as well as their
        locations.  If there are enough users to begin the game, it initializes
        the game variables. 
        """
        if self.user_count < const.lobby_size:
            self.user_count += 1
            self.user_coords.append((lat, lon))
            if self.user_count == const.lobby_size:
                self.start_game()
            return self.user_count-1
        else:
            return -1

    def update_user(self, id, lon, lat):
        gridloc = project(lon, lat)
        out_of_bounds = check_grid_range(gridloc[0], gridloc[1])
        
        if not out_of_bounds:
            self.grid[gridloc] = const.Team.findTeam(id)

        returngrid =  diff(grid, self.user_grid[id])
        self.user_grid[id] = self.grid
        return returngrid, out_of_bounds

    def check_grid_range(self, coord):
        return coord[0] >= 0 and coord[1] >=0 and coord[0] < const.radius*2+1 and coord[1] < const.radius*2+1
         
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
