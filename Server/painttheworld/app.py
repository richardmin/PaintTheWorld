# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask import Flask
from flask_restful import Api
from painttheworld.api import Reset, Lobby, GameData

app = Flask(__name__)
api = Api(app)

# bind the APIs
api.add_resource(GameData, '/game_data')
api.add_resource(Lobby, '/join_lobby')
api.add_resource(Reset, '/reset')
