# painttheworld/app.py
#
# Creates and exports a flask app object and defines some
# endpoints to serve.

__all__ = [ 'app' ]

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/debug')
def debug():
    return render_template('debug.html')
