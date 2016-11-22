# painttheworld/game.py
#
# Represent and track the current game state.

import numpy as np
import datetime
import math
from painttheworld import constants
from painttheworld.constants import m1, m2, m3, m4, p1, p2, p3

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
        self.user_grid.extend([self.grid for i in range(constants.lobby_size)])

    def start_game(self):
        """Initialize the starting position of the grid.

        This calculates the center coordinate by average the longitudes and
        latitudes of all people (this might not work too well, as that's not
        really how nautical miles work). Additionally, it sets the start time to
        be 3 seconds from now.
        """
        self.center_coord = np.mean(self.user_coords, axis=1)
        self.conversion_rates = self.conversion_rates(self.center_coord)
        self.start_time = datetime.datetime.now() + datetime.timedelta(seconds=3)
        self.end_time = self.start_time + datetime.timedelta(minutes=3)

    def update(self, coord, team):
        """Update the game state array."""
        x, y = coord
        self.grid[x][y] = team

    def project(self, lon, lat):
        """ Casts a GPS coordinate onto the grid, which has it's central
        locations defined by center_coord.
        """
        vert = GameState.haversine(self.center_coord[0], self.center_coord[1], self.center_coord[0], lat) # longitude is east-west, we ensure that's the sam'
        horiz = GameState.haversine(self.center_coord[0], self.center_coord[1], lon, self.center_coord[1])

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

        horiz = math.floor(horiz * 1000 / constants.gridsize)
        vert = math.floor(vert * 1000 / constants.gridsize)

        return np.add((self.radius + 1, self.radius + 1), (horiz, vert))

    def add_user(self, lat, lon):
        """ Adds a user and their starting location to the grid.

        Returns the user id number assosciated with that user, as well as their
        locations.  If there are enough users to begin the game, it initializes
        the game variables. 
        """
        if self.user_count < constants.lobby_size:
            self.user_count += 1
            self.user_coords.append((float(lat), float(lon)))
            if self.user_count == constants.lobby_size:
                self.start_game()
            return self.user_count-1
        else:
            return -1

    def update_user(self, id, lon, lat):
        currtime = datetime.datetime.now()
        if self.start_time < currtime < self.end_time: 
            gridloc = self.project(lon, lat)
            out_of_bounds = self.check_grid_range(gridloc)
            
            if not out_of_bounds:
                self.grid[gridloc] = constants.Team.findTeam(id)

            returngrid =  self.diff(self.user_grid[id], self.grid)
            self.user_grid[id] = self.grid
            return returngrid, out_of_bounds
        else:
            if self.start_time > currtime:
                raise RuntimeError('Game hasn\'t started.')
            else:
                raise RuntimeError('Game over.')

    def check_grid_range(self, coord):
        return coord[0] >= 0 and coord[1] >=0 and coord[0] < constants.radius*2+1 and coord[1] < constants.radius*2+1
         
    @staticmethod
    def diff(a, b):
        """Calculate the deltas of two GameState objects.
            a is the "older" GameState object
            b is the "updated" GameState object

        Returns:
            List of coordinate/team pairings of the form ((x,y), team_color).
        """
        diff = np.absolute(a - b)
        coord = np.nonzero(diff)
        val = diff[coord]
        coord = map(tuple, np.transpose(coord))  # turn coord into (x,y) tuples
        return list(zip(coord, val))

    @staticmethod
    def conversion_rates(coord):
        """Calculates the conversion rate for 1 degree of longitude to a variety
        of measurements, returned in a dict. 
            
        Args: 
            coord: a tuple (longitude, latitude) 
        Returns:
            Conversion rate for 1 degree of longitude to miles
        """
        latitude = math.radians(coord[1])
        dict = {}

        latlen = m1 + ( m2 * math.cos(2 * latitude) + \
                        m3 * math.cos(4 * latitude) + \
                        m4 * math.cos(6 * latitude)   \
                      )

        longlen = (p1 * math.cos(1 * latitude)) + \
                  (p2 * math.cos(3 * latitude)) + \
                  (p3 * math.cos(5 * latitude))

        dict['lat_meters'] = latlen
        dict['lat_feet'] = latlen * 3.28083333
        dict['lat_miles'] = dict['lat_feet'] / 5280
        
        dict['long_meters'] = longlen
        dict['long_feet'] = longlen * 3.28083333
        dict['long_miles'] = dict['long_feet'] / 5280

        return dict

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        Source code from: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        km = 6367 * c
        return km
