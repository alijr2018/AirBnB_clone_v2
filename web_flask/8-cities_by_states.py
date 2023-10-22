#!/usr/bin/python3
"""
Start a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a list of states and their cities."""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
