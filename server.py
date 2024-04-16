"""Server for productivity app."""

from flask import (Flask, render_template, jsonify, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined

from model import connect_to_db, db, Event, RecurEvent, Routine, Tasklist, RecurTasklist
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def show_homepage():
    """Create the homepage."""

    return render_template("homepage.html")

@app.route("/create-account", methods=["POST"])
def create_account():
    """Creates a new account."""
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    email_exists = crud.check_email_exists(email)

    if email_exists:
        flash("Account with this email already exists.")
        return redirect("/")
    else:
        user = crud.create_user(email, password, username, None)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        return redirect("/")

@app.route("/login", methods=["POST"])
def log_in():
    """Login a user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.check_credentials(email, password)

    if user:
        session["user_id"] = user.user_id
        return redirect("/dashboard")
    
    flash("Email or password incorrect, please try again.")
    return redirect("/")

@app.route("/dashboard")
def show_user_dashboard():
    """Create user dashboard."""
    
    user = crud.get_user_by_id(session["user_id"])
    todays_tasklists = crud.get_todays_tasklists()
    todays_events = crud.get_todays_events()
    
    return render_template("dashboard.html", username=user.username,
                           todays_tasklists=todays_tasklists,
                           todays_events=todays_events)

@app.route("/month")
def show_monthly_schedule():
    """Create user monthly schedule."""
    
    user = crud.get_user_by_id(session["user_id"])
    
    return render_template("month.html", username=user.username)

@app.route("/delete")
def show_delete_option():
    """Create page with the option to delete an event."""
    
    return render_template("delete.html")

@app.route("/api/add-event")
def add_event():
    """Adds a user-created event to the calendar."""

    items = []
    
    for event in Event.query.all():
        items.append({
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

    for recur_event in RecurEvent.query.all():
        items.append({
            "title": recur_event.title,
            "allDay": recur_event.all_day,
            "start": recur_event.start,
            "end": recur_event.end,
            "url": recur_event.url,
            "display": recur_event.display,
            "backgroundColor": recur_event.background_color,
            "borderColor": recur_event.border_color,
            "textColor": recur_event.text_color,
            "daysOfWeek": recur_event.days_of_week,
            "startRecur": recur_event.start_recur,
            "endRecur": recur_event.end_recur
        })

    return jsonify(items)


@app.route("/create-event")
def create_new_event():
    """Creates a new event."""
    
    # Get user input for event
    title = request.args.get("event-title")
    start_date = request.args.get("start-date")
    start_time = request.args.get("start-time")
    end_date = request.args.get("end-date")
    end_time = request.args.get("end-time")
    all_day = request.args.get("all-day")
    repeat = request.args.get("repeat-option")
    # TODO: Get user input for recurring events
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("event-repeat-start")
    end_recur = request.args.get("event-repeat-end")

    # Convert dates/times into strings
    start = crud.get_date_str(start_date, start_time)
    end = crud.get_date_str(end_date, end_time)

    # Initalize user and default display
    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    if repeat is None:
        crud.create_event(title, all_day, start, end, "", "", url, display,
                 background_color, border_color, text_color, None, None,
                 completed, user)
    else:
        crud.create_recur_event(title, all_day, start, end, "", "", url, display,
                 background_color, border_color, text_color, days_of_week, start_recur, end_recur, None, None,
                 completed, user)

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
