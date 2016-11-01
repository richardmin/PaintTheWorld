# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask import Flask, render_template, request
import game

app = Flask(__name__)
app.config.from_object('config')

@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/game_data', methods=['POST'])
def game_data():
    # TODO: return actual JSON object
    # request.form['location']
    # request.form['magic']
    return '{fake json object, with updated data}'

# TODO: Support multiple lobbies, probably in own file later
@app.route('/join_lobby', methods=['GET', 'POST'])
def join_lobby():
    if request.method == 'POST'
        user_count++; 
    return '{users: \'{0}\', game_start_time: \'{1}\'}'.format(user_count, start_time)
