# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask import Flask, render_template, request
from painttheworld.game import GameState

app = Flask(__name__)
app.config.from_object('config')

radius = 50 #2500 tiles
gridsize = 5 #5 feet per tile. 

active_game = None

def validate_longitude(longitude):
    return longitude >= -180 and longitude <= 180
def validate_latitude(latitude):
    return latitude >= -90 and latitude <= 90

@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/game_data', methods=['POST'])
def game_data():
    global active_game
    if 'user-id' not in request.form.to_dict() or 'long' not in request.form.to_dict() or 'lat' not in request.form.to_dict():
        return '{error: \'data format invalid\'}'
    if active_game is None or active_game.start_time is None:
        return '{error: \'No Game In Progress\'}'
    if request.form['user-id'] < 0 or request.form['user-id'] >= game.lobby_size:
        return '{error: \'Invalid user id\'}'

    if not validate_latitude(request.form['lat']):
        return '{error: \'Invalid latitude degree\'}'
    if not validate_longitude(request.form['long']):
        return '{error: \'Invalid longitude degree\'}'

    if request.form['id'] >= game.lobby_size or request.form['id'] < 0:
        return '{error: \'Invalid user id\'}'
    
    
    
    active_game.update_user(request.form['id'], request.form['long'], request.form['lat'])


    return '{{}}'

# TODO: Support multiple lobbies, probably in own file later
@app.route('/join_lobby', methods=['GET', 'POST'])
def join_lobby():
    global active_game, radius, gridsize
    if request.method == 'POST':
        if 'lat' not in request.form.to_dict():
            return '{error: \'lat field not found\'}'
        if 'long' not in request.form.to_dict(): 
            return '{error: \'long field not found\'}'
        if not validate_latitude(request.form['lat']):
            return '{error: \'Invalid latitude degree\'}'
        if not validate_longitude(request.form['long']):
            return '{error: \'Invalid longitude degree\'}'
        if active_game is None:
            active_game = GameState(radius, gridsize) 
         
        usernum = active_game.add_user(request.form['lat'], request.form['long'])
        
        if active_game.user_count is game.lobby_size:
            return '{{user-id: {0}, user-count: {1}, game_start_time: {2}}}'.format(usernum, active_game.user_count, active_game.start_time.isoformat())
        else:
            return '{{user-id: {0}, user-count: {1}}}'.format(usernum, active_game.user_count)
        
    if active_game is None:
        return '{error: \'No game in progress\'}'
    elif active_game.user_count < game.lobby_size:
        return '{{user-count: {0}}}'.format(active_game.user_count)
    return '{{user-count: {0}, game_start_time: {1}}}'.format(active_game.user_count, active_game.start_time.isoformat())
