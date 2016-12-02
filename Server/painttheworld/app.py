# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask import Flask, render_template, request, json
from flask_restful import reqparse, Resource, Api
from painttheworld import constants
from painttheworld.constants import active_game
from painttheworld.game import GameState

app = Flask(__name__)
api = Api(app)

def validate_coordinates(coord):
    lon, lat = coord
    return -180 <= lon <= 180 and -90 <= lat <= 90

# /reset endpoint
# clears the server's gamestate
class Reset(Resource):
    def get(self):
        global active_game
        active_game = None
        return {'message': 'Reset successful, thank you for your business.'}

# /game_date endpoint
class GameData(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user-id', type=int, location='json', required=True)
        self.parser.add_argument('long', type=float, location='json', required=True)
        self.parser.add_argument('lat', type=float, location='json', required=True)

    # retrieve new location from client (with input sanitization)
    # - update the server's copy of the gamestate with any new state changes
    # - return a list of gamestate changes to the client
    def post(self):
        args = self.parser.parse_args()
        if active_game is None or active_game.start_time is None:
            return {'error': 'No game in progress.'}, 200
        elif args['user-id'] < 0 or args['user-id'] >= constants.lobby_size:
            return {'error': 'Invalid user id.'}, 400
        elif not validate_coordinates((args['long'], args['lat'])):
            return {'error': 'Invalid coordinates.'}, 400
        
        try:
            deltas, out_of_bounds = active_game.update_user(
                args['user-id'],
                args['long'],
                args['lat']
            )
        except RuntimeError as e:
            return {'error': e.args[0]}, 200

        resp = {}
        if out_of_bounds:
            resp['out-of-bounds'] = True
        resp['grid-deltas'] = [self.fmt_diff(coord, team) for coord, team in deltas]
        return resp

    @staticmethod
    def fmt_diff(coord, team):
        x, y = coord
        return {
            'coord': {'x': x.item(), 'y': y.item()},
            'color': team.item()
        }


# /join_lobby endpoint
class Lobby(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('lat', type=float, location='json', required=True)
        self.parser.add_argument('long', type=float, location='json', required=True)

    # client has requested to join game, take their coordinates and add them to
    # the lobby of users waiting for the game to start
    def post(self):
        global active_game
        args = self.parser.parse_args()
        if not validate_coordinates((args['long'], args['lat'])):
            return {'error': 'Invalid coordinates'}, 400
        if active_game is None:
            active_game = GameState(constants.radius, constants.gridsize)

        usernum = active_game.add_user(args['lat'], args['long'])

        resp = {
            'user-id': usernum,
            'user-count': active_game.user_count
        }
        
        return resp

    # once the game has started, return information about the game including
    # - when the game starts
    # - where to center the grid on the map (average of all user's coordinates)
    # - how big to make the grid and grid tiles
    def get(self):
        if active_game is None:
            return {'error': 'No game in progress.'}, 400

        resp = {
            'user-count': active_game.user_count
        }
        if active_game.user_count == constants.lobby_size:
            resp['game-start-time'] = active_game.start_time.isoformat()
            resp['center-coord-x'] = active_game.center_coord[0]
            resp['center-coord-y'] = active_game.center_coord[1]
            resp['radius'] = constants.radius
            resp['gridsize-longitude'] = 1 / active_game.conversion_rates['lat_meters'] * constants.gridsize 
            resp['gridsize-latitude'] = 1 / active_game.conversion_rates['long_meters'] * constants.gridsize
        return resp

# bind the APIs
api.add_resource(GameData, '/game_data')
api.add_resource(Lobby, '/join_lobby')
api.add_resource(Reset, '/reset')
