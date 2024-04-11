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
    # Icon TBD
    # Icon color TBD

    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    event = crud.create_event(title, False, start, end, "", "", url, display,
                 background_color, border_color, text_color, None, None,
                 completed, user)
    
    db.session.add(event)
    db.session.commit()

    return redirect("/dashboard")


@app.route("/create-routine")
def create_new_routine():
    """Creates a new routine."""
    title = request.args.get("title")
    start = request.args.get("start")
    end = request.args.get("end")

    return redirect("/dashboard")


@app.route("/create-tasklist")
def create_new_tasklist():
    """Creates a new tasklist."""
    title = request.args.get("title")
    start = request.args.get("date")
    
    all_day = True
    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    tasklist = crud.create_tasklist(title, all_day, start, url, display,
                 background_color, border_color, text_color, None, None,
                 completed, user)
    
    db.session.add(tasklist)
    db.session.commit()

    # TODO: 
    for i in range(5):
        task_title = request.args.get(f"task{1}")
        
        display = "auto"
        background_color = "blue"
        border_color = "black"
        text_color = "black"
        completed = False
        
        task = crud.create_task(task_title, display, background_color, border_color,
                                text_color, None, None, completed, tasklist)
        
        db.session.add(task)
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
