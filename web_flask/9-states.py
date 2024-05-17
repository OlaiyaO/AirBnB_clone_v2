#!/usr/bin/python3
"""
Launches a Flask web app listening on 0.0.0.0:5000.
Routes:
    /states: Displays all State objects.
    /states/<id>: Displays the state with <id>.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """
    Renders an HTML page with all States.
    """
    states = storage.all("State")
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    Renders an HTML page with the state <id> if it exists.
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """
    Closes the current SQLAlchemy session.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
