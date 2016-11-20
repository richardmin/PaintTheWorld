# painttheworld/game.py
#
# Represent and track the current game state.

import numpy as np
import datetime
import math
from painttheworld.constants.GPS import m1, m2, m3, m4, p1, p2, p3

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

    def start_game(self):
        """Initialize the starting position of the grid.

        This calculates the center coordinate by average the longitudes and
        latitudes of all people (this might not work too well, as that's not
        really how nautical miles work). Additionally, it sets the start time to
        be 3 seconds from now.
        """
        self.center_coord = np.mean(self.user_coords, axis=1)
        self.longitude_conversion = self.calculateLongitude(self.center_coord)
        self.start_time = (datetime.datetime.now() + datetime.timedelta(seconds=3))

    def update(self, coord, team):
        """Update the game state array."""
        x, y = coord
        self.grid[x][y] = team

    def convert(self, lon, lat):
        """ Casts a GPS coordinate onto the grid, which has it's central
        locations defined by center_coord.
        """
        vert = haversine(self.center_coord[0], self.center_coord[1], self.center_coord[0], lat) # longitude is east-west, we ensure that's the sam'
        horiz = haversine(self.center_coord[0], self.center_coord[1], lon, self.center_coord[1])

        """ Vectorizes the latitude. The degree ranges from -90 to 90.
            This latitude conversion doesn't handle poles.
        """
        #if lat > self.center_coord[1]:
        #    vert = -vert

        #if self.center_coord[0] >= 0 and lon >= 0:
        #    if lon < self.center_coord:
        #        horiz = -horiz
        #elif self.center_coord[0] < 0 and lon < 0:
        #    if lon < self.center_coord:
        #        horiz = -horiz
        #elif self.center_coord[0] < 0 and lon > 0:
        #
        #elif self.center_coord[0] > 0 and lon < 0:

        vert = vert/self.gridsize + 25
        horiz = horiz/self.gridsize + 25

        return vert, horiz
    
    def add_user(self, lat, lon):
        """ Adds a user and their starting location to the grid.

        Returns the user id number assosciated with that user, as well as their
        locations.  If there are enough users to begin the game, it initializes
        the game variables. 
        """
        if self.user_count < lobby_size:
            self.user_count += 1
            self.user_coords.append((lat, lon))
            if self.user_count == lobby_size:
                self.start_game()
            return self.user_count-1
        else:
            return -1

    # def update_user(self, id, lat, lon):
    #     # update the user
    #     self.grid[]

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

        latlen = m1 + (m2 * math.cos(2 * latitude) +
                      (m3 * math.cos(4 * latitude)) +
                      (m4 * math.cos(6 * latitude)))

        longlen = (p1 * math.cos(latitude)) +
                  (p2 * math.cos(3 * latitude)) +
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
