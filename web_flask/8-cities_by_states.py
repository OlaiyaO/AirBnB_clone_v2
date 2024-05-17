#!/usr/bin/python3
"""
Launches a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /cities_by_states: Displays a list of states and their cities.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Renders an HTML page with a list of states and their cities.
    """
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """
    Closes the current SQLAlchemy session.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
