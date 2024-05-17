#!/usr/bin/python3
"""
Launches a Flask web app listening on 0.0.0.0:5000.
Routes:
    /hbnb: Displays the HBnB home page.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Renders the HBnB home page.
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template(
            "100-hbnb.html",
            states=states,
            amenities=amenities,
            places=places)


@app.teardown_appcontext
def teardown(exc):
    """
    Closes the current SQLAlchemy session.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
