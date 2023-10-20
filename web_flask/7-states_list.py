#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__, template_folder='templates')

@app.route('/', strict_slashes=False)
def hello_hbnb():
    return ("Hello HBNB!")

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return ("HBNB")

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')
    return ("C {}".format(text))

@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    text = text.replace('_', ' ')
    return ("Python {}".format(text))

@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return ("{} is a number".format(n))

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return (render_template('5-number.html', n=n))

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    result = "even" if n % 2 == 0 else "odd"
    return (render_template('6-number_odd_or_even.html', n=n, result=result))

@app.route('/states_list', strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
