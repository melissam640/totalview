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

@app.route("/add-new")
def show_add_item_options():
    """Create page with options to add new event."""
    
    return render_template("add-new.html")

@app.route("/delete")
def show_delete_option():
    """Create page with the option to delete an event."""
    
    return render_template("delete.html")

@app.route("/api/add-event")
def add_event():
    """Adds a user-created event to the calendar."""

    events = []
    for event in Event.query.all():
        events.append({
            "title": event.title,
            "allDay": event.all_day,
            "start": event.start,
            "end": event.end,
            "url": event.url,
            "display": event.display,
            "backgroundColor": event.background_color,
            "borderColor": event.border_color,
            "textColor": event.text_color
        })

    return jsonify(events)


@app.route("/create-event")
def create_new_event():
    """Creates a new event."""
    title = request.args.get("title")
    start = request.args.get("start")
    end = request.args.get("end")

    event = crud.create_event(title, False, start, end, "", "", "/", "auto",
                 None, None, "black", None, None,
                 False, None)
    
    db.session.add(event)
    db.session.commit()

    return redirect("/dashboard")


@app.route("/delete-event")
def delete_event():
    """Deletes an event."""
    
    title = request.args.get("delete")
    crud.delete_event(title)
    
    return redirect("/dashboard")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
