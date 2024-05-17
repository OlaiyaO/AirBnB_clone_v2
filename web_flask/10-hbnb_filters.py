#!/usr/bin/python3
"""
Launches a Flask web app listening on 0.0.0.0:5000.
Routes:
    /hbnb_filters: Displays the HBnB filters page.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Renders the HBnB filters HTML page.
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template(
            "10-hbnb_filters.html",
            states=states,
            amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """
    Closes the current SQLAlchemy session.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
