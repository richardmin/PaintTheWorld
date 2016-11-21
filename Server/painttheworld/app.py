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
app.config.from_object('config')
api = Api(app)

@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/reset')
def reset():
    global active_game
    active_game = None
    
def validate_coordinates(coord):
    lon, lat = coord
    return -180 <= lon <= 180 and -90 <= lat <= 90

class GameData(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user-id', type=int, required=True)
        self.parser.add_argument('long', type=float, required=True)
        self.parser.add_argument('lat', type=float, required=True)

    def post(self):
        args = self.parser.parse_args()
        
        if active_game is None or active_game.start_time is None:
            return {'error': 'No game in progress.'}, 400
        elif args['user-id'] < 0 or args['user-id'] >= constants.lobby_size:
            return {'error': 'Invalid user id.'}, 400
        elif not validate_coordinates((args['long'], args['lat'])):
            return {'error': 'Invalid coordinates.'}, 400
        
        return_deltas, out_of_bounds = active_game.update_user(args['user-id'],
                                             args['long'],
                                             args['lat'])
        resp = {}
        if out_of_bounds:
            resp['out-of-bounds'] = True
        return_deltas = [[(1, 2), constants.Team.RED]]
        
        resp['grid-deltas'] = [{'coord': {'x': 1, 'y': 2}, 'color': 1}]


        return resp

# TODO: Support multiple lobbies, probably in own file later
# TODO: Make a game manager class that is in charge of cycling game state (a
# game statemachine basically)
class Lobby(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('lat', type=float, required=True)
        self.parser.add_argument('long', type=float, required=True)

    def post(self):
        global active_game
        args = self.parser.parse_args()
        if not validate_coordinates((args['long'], args['lat'])):
            return {'error': 'Invalid coordinates'}, 400
        if active_game is None:
            active_game = GameState(constants.radius, constants.gridsize)

        usernum = active_game.add_user(args['lat'], args['long'])
        return {
            'user-id': usernum,
            'user-count': active_game.user_count
        }

    def get(self):
        if active_game is None:
            return {'error': 'No game in progress.'}, 400

        resp = {
            'user-count': active_game.user_count
        }
        if active_game.user_count == constants.lobby_size:
            resp['game-start-time'] = active_game.start_time.isoformat()
            resp['center-coord'] = active_game.center_coord
            resp['radius'] = constants.radius
            resp['gridsize'] = active_game.conversion_rates['lat_meters'] * constants.gridsize
        return resp

# bind the APIs
api.add_resource(GameData, '/game_data')
api.add_resource(Lobby, '/join_lobby')
