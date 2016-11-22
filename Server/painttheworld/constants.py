from enum import IntEnum

# Game-related constants
radius = 50    # 2500 tiles
gridsize = 5   # 5 feet per tile
lobby_size = 6
active_game = None

# GPS-related constants
m1 = 111132.92  # latitude calculation term 1
m2 = -559.82    # latitude calculation term 2
m3 = 1.175      # latitude calculation term 3
m4 = -0.0023    # latitude calculation term 4
p1 = 111412.84  # longitude calculation term 1
p2 = -93.5      # longitude calculation term 2
p3 = 0.118      # longitude calculation term 3

# Teams
class Team(IntEnum):
    NONE = 0
    RED  = 1
    BLUE = 2
    
    @staticmethod
    def findTeam(userid):
        return 1 if userid < lobby_size/2 else 2


m1 = 111132.92  # latitude calculation term 1
m2 = -559.82    # latitude calculation term 2
m3 = 1.175      # latitude calculation term 3
m4 = -0.0023    # latitude calculation term 4
p1 = 111412.84  # longitude calculation term 1
p2 = -93.5      # longitude calculation term 2
p3 = 0.118      # longitude calculation term 3