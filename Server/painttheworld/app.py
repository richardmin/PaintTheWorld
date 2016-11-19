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
@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/game_data', methods=['POST'])
def game_data():
    global active_game
    userid = request.form['user-id']

    # request.form['location']
    # request.form['magic'] 
    return '{{fake json object, with updated data}}'

# TODO: Support multiple lobbies, probably in own file later
@app.route('/join_lobby', methods=['GET', 'POST'])
def join_lobby():
    global active_game, radius, gridsize
    if request.method == 'POST':
        
        if 'lat' not in request.form.to_dict():
            return '{error: \'lat field not found\'}'
        if 'long' not in request.form.to_dict():
            return '{error: \'long field not found\'}'
        if active_game is None:
            active_game = GameState(radius, gridsize) 
         
        usernum = active_game.add_user(request.form['lat'], request.form['long'])
        
        if usernum is 8:
            return '{{user-id: {0}, user-count: {1}, game_start_time: {3}}}'.format(usernum, active_game.get_user_count(), active_game.get_start_time())
        else:    
            return '{{user-id: {0}, user-count: {1}}}'.format(usernum, active_game.get_user_count())
        
    if active_game is None:
        return '{error: \'No game in progress\'}'
    elif active_game.get_user_count() < 8:
        return '{{user-count: {0}}}'.format(active_game.get_user_count())
    return '{{user-count: {0}, game_start_time: {1}}}'.format(active_game.get_user_count(), active_game.get_start_time())
