"""Server for productivity app."""

from flask import (Flask, render_template, jsonify, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined

from model import connect_to_db, db, Event
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def show_homepage():
    """Create the homepage."""

    return render_template("homepage.html")

@app.route("/dashboard")
def show_user_dashboard():
    """Create user dashboard."""
    
    return render_template("dashboard.html")

@app.route("/api/add-event")
def add_event():
    """Adds a user-created event to the calendar."""

    events = [{
        "allDay": False,
        "end": "2024-04-05T15:30:00",
        "start": "2024-04-05T14:30:00",
        "title": "Event Title"},
        {
        "allDay": True,
        "end": "2024-04-10",
        "start": "2024-04-10",
        "title": "Second Event"
        }]

    return jsonify(events)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
