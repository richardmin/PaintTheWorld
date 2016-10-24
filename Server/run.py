#!/usr/bin/env python3
#
# Start the development server.

from painttheworld import app
app.run(
    host='localhost',
    port= 5000,
    debug=True
)
