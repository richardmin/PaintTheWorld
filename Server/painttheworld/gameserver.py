# painttheworld/game.py
#
# Represent and track the current game state.
# Helpful note: latitude is North/South and longitude is East/West

import math
import datetime
import numpy as np
from painttheworld import const
from painttheworld.grid import Grid
from painttheworld.coord import conversion_rates, haversine

class OutOfBoundsException(Exception):
    pass

class User:
    def __init__(self, coord):
        """Creates a new user with a grid state and a current coordinate.

        Arguments:
            coord: a (latitude, longitude) pair
        """
        self.grid = Grid()
        self.coord = coord

class GameServer:
    """Keeps track of which teams have colored which areas of the map.

    The map is a grid that's represented by a 2D array containing values
    corresponding to which team controls that area/block of the map.  Clients
    perform the necessary GPS -> grid coordinate calculations and send their
    game state updates in grid coordinates via the update() method.

    TODO: might have to add coordinate transformations to our methods since
          (0,0) is technically the center of our grid.
    """

    def __init__(self):
        """Create a GameState object. """
        self.users = {}
        self.grid = Grid()
        self.running = False

    def start_game(self):
        """Initialize the starting position of the grid.

        This calculates the center coordinate by averaging the longitudes and
        latitudes of all users. Additionally, it sets the start time to
        be 3 seconds from now.
        """
        self.running = True
        self.center_coord = np.mean(
            [user.coord for _, user in self.users.items()],
            axis=0
        )
        for i, (_, user) in enumerate(self.users.items()):
            print('user ', i, ': ', user.coord)
        print('avg: ', self.center_coord)
        self.conversion_rates = conversion_rates(self.center_coord)
        self.start_time = datetime.datetime.now() + datetime.timedelta(seconds=3)
        self.end_time = self.start_time + datetime.timedelta(minutes=1)

    def add_user(self, coord):
        """ Adds a user and their starting location to the grid.

        Args:
            coord: a (latitude, longitude) pair
        Returns:
            an integer ID token that can be used to send further updates.
        """
        if self.running:
            return -1

        id = len(self.users)
        self.users[id] = User(coord)

        if len(self.users) == const.MAX_USERS:
            self.start_game()
            return -1

        return id

    def update_user(self, id, gps_coord):
        curtime = datetime.datetime.now()
        if curtime < self.start_time:
            raise RuntimeError('Waiting for game to start.')
            return
        elif curtime > self.end_time:
            raise RuntimeError('Game over.')
            return

        info = {}
        user = self.users[id]
        gridloc = self.project(gps_coord)

        in_bounds = self.grid.inside_grid(gridloc)
        if in_bounds:
            self.grid.array[gridloc] = const.Team.findTeam(id)

        deltas = Grid.diff(user.grid, self.grid)
        np.copyto(user.grid.array, self.grid.array)

        return deltas, in_bounds

    def project(self, gps_coord):
        """Casts a GPS coordinate onto the grid plane, which has its central
           locations defined by 'center'. May return an OutOfBoundsException if
           the given gps_coordinate misses the game grid."""

        lat, lon = gps_coord
        center_lat, center_lon = self.center_coord

        vert = haversine(self.center_coord, (lat, center_lon))
        horiz = haversine(self.center_coord, (center_lat, lon))
        """ Vectorizes the latitude. The degree ranges from -90 to 90.
            This latitude conversion doesn't handle poles.
            I'm not sure how to handle you playing the game at the north and
            south pole.
        """ 
        if lat > center_lat:
            vert = -vert

        """ Vectorizes the longitude. The degree ranges from -180 to 180.
            There's three cases: 
                1. They're both in the same hemisphere (east/west)
                2. They cross over the 0 degree line
                3. They cross over the 180 degree line
            
            Case (1):
                Check for case 1 by ensuring that the signs are identical.
                If the longitude of the location is less than the longitude of
                the cenral location, that means that we need to move left in the
                array.  We change the sign to be negative.

            Case (2) + (3):
                There's two cases here, where the signs are differing. 
                To determine which line we're crossing, the absolute value of
                the difference in longitudes is taken. If the difference >180, 
                that implies that the 180 degree is being crossed. Otherwise,
                it's the 0 degree line.

            Case (2):
                In case (2), if the longitude of the central point is negative,
                the distance must be positive.  If the longitude of the central
                point is positive, the distance must be negative.
            
            Case (3):
                In case (3), if the longitude of the central point is negative,
                the distance must be negative.  If the longitude of the central
                point is positive, the distance must be positive.

        """
        if np.sign(center_lon) == np.sign(lon): # Case 1
            if lon > center_lon:
                horiz = -horiz
        if math.fabs(center_lon - lon) < 180: # Case 2
            if center_lon >= 0:
                horiz = -horiz
        elif center_lon < 0: # Case 3
            horiz = -horiz

        horiz = math.floor(horiz * 1000 / const.GRIDSIZE)
        vert = math.floor(vert * 1000 / const.GRIDSIZE)

        grid_center = (const.RADIUS + 1, const.RADIUS + 1)
        grid_coord = np.add(grid_center, (horiz, vert))
        return grid_coord
