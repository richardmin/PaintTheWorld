# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask_restful import Resource, reqparse, fields, marshal_with
from painttheworld import const
from painttheworld.gameserver import GameServer

game = GameServer()


# functions used to validate input.
def latitude(lat):
    if not -90 <= float(lat) <= 90:
        raise ValueError("Improper latitude, not within -90 to 90 degrees.")
    return lat

def longitude(lon):
    if not -90 <= float(lon) <= 90:
        raise ValueError("Improper longitude, not within -180 to 180 degrees.")
    return lon

def userID(id):
    if not 0 <= int(id) <= const.MAX_USERS:
        raise ValueError("Invalid user id.")
    return id

class Reset(Resource):
    def get(self):
        game.reset()
        return {
            'message': 'Reset successful, thank you for your business.'
        }


class GameData(Resource):
    # JSON response structure
    delta = {
        'coord': {
            'x': fields.Float,
            'y': fields.Float
        },
        'team': fields.Integer
    }
    response = {
        'grid-deltas': fields.List(fields.Nested(delta)),
        'out-of-bounds': fields.Boolean,
        'error': fields.String
    }

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'user-id', type=userID,
             location='json', required=True
        )
        self.parser.add_argument(
            'lat', type=latitude,
            location='json', required=True
        )
        self.parser.add_argument(
            'long', type=longitude,
            location='json', required=True
        )

    @marshal_with(response)
    def post(self):
        args = self.parser.parse_args()
        if not game.running:
            return {'error': 'No game in progress.'}, 200
        
        try:
            gps_coord = (args['lat'], args['long'])
            deltas, in_bounds = game.update_user(args['user-id'], gps_coord)
        except RuntimeError as error:
            return {'error': str(error)}, 400

        resp = {
            'out-of-bounds': not in_bounds,
            'grid-deltas': [self.fmt_diff(loc, team) for loc, team in deltas]
        }
        return resp

    @staticmethod
    def fmt_diff(coord, team):
        x, y = coord
        return {
            'coord': {'x': x.item(), 'y': y.item()},
            'color': team.item()
        }


class Lobby(Resource):
    post_response = {
        'user-id': fields.Integer,
        'user-count': fields.Integer,
    }
    get_response = {
        'user-count': fields.Integer,
        'game-start-time': fields.DateTime(dt_format='iso8601'),
        'center-coord-x': fields.Float,
        'center-coord-y': fields.Float,
        'radius': fields.Integer,
        'gridsize-longitude': fields.Float,
        'gridsize-latitude': fields.Float,
        'error': fields.String
    }

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'lat', type=latitude,
            location='json', required=True,
            help='Invalid latitude.'
        )
        self.parser.add_argument(
            'long', type=longitude,
            location='json', required=True,
            help='Invalid longitude.'
        )
        
    @marshal_with(post_response)
    def post(self):
        args = self.parser.parse_args()
        id = game.add_user((args['lat'], args['long']))

        return {
            'user-id': id,
            'user-count': len(game.users)
        }

    @marshal_with(get_response)
    def get(self):
        if not game.running:
            return {'error': 'No game in progress.'}, 400

        resp = {
            'user-count': active_game.user_count
        }
        if active_game.user_count == const.lobby_size:
            resp['game-start-time'] = game.start_time.isoformat()
            resp['center-coord-x'] = game.center_coord[0]
            resp['center-coord-y'] = game.center_coord[1]
            resp['radius'] = const.radius
            resp['gridsize-longitude'] = 1 / game.conversion_rates['lat_meters'] * const.gridsize 
            resp['gridsize-latitude'] = 1 / game.conversion_rates['long_meters'] * const.gridsize
        return resp
