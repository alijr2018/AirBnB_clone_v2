#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template

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
    return render_template('6-number_odd_or_even.html', n=n, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
