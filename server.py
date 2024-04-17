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
    todays_recur_tasklists = crud.get_todays_recur_tasklists()
    todays_events = crud.get_todays_events()
    todays_recur_events = crud.get_todays_recur_events()
    todays_routines = crud.get_todays_routines()
    
    return render_template("dashboard.html", username=user.username,
                           todays_tasklists=todays_tasklists,
                           todays_recur_tasklists=todays_recur_tasklists,
                           todays_events=todays_events,
                           todays_recur_events=todays_recur_events,
                           todays_routines=todays_routines)

@app.route("/month")
def show_monthly_schedule():
    """Create user monthly schedule."""
    
    user = crud.get_user_by_id(session["user_id"])
    
    return render_template("month.html", username=user.username)

@app.route("/delete")
def show_delete_option():
    """Create page with the option to delete an event."""
    
    return render_template("delete.html")

@app.route("/account")
def show_user_account():
    """Creates page with user account infomation."""

    user = crud.get_user_by_id(session["user_id"])

    return render_template("/account", username=user.username)

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
        
        # Convert days of week from string to list if it's not None
        if recur_event.days_of_week:
            days_of_week = recur_event.days_of_week.split(" ")
        else:
            days_of_week = recur_event.days_of_week
        
        items.append({
            "title": recur_event.title,
            "allDay": recur_event.all_day,
            "startTime": recur_event.start,
            "endTime": recur_event.end,
            "url": recur_event.url,
            "display": recur_event.display,
            "backgroundColor": recur_event.background_color,
            "borderColor": recur_event.border_color,
            "textColor": recur_event.text_color,
            "daysOfWeek": days_of_week,
            "startRecur": recur_event.start_recur,
            "endRecur": recur_event.end_recur
        })

    for routine in Routine.query.all():
        
        # Convert days of week from string to list if it's not None
        if routine.days_of_week:
            days_of_week = routine.days_of_week.split(" ")
        else:
            days_of_week = routine.days_of_week
        
        items.append({
            "title": routine.title,
            "startTime": routine.start,
            "endTime": routine.end,
            "url": routine.url,
            "display": routine.display,
            "backgroundColor": routine.background_color,
            "borderColor": routine.border_color,
            "textColor": routine.text_color,
            "daysOfWeek": days_of_week,
            "startRecur": routine.start_recur,
            "endRecur": routine.end_recur
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
    repeat = request.args.get("event-repeat-option")
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("event-repeat-start")
    end_recur = request.args.get("event-repeat-end")

    # Initalize user and default display settings
    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])
    
    if repeat == "none": # Create a one-time event

        start = crud.get_date_str(start_date, start_time)
        end = crud.get_date_str(end_date, end_time)
        
        crud.create_event(title, all_day, start, end, "", "", url, display,
                 background_color, border_color, text_color, None, None,
                 completed, user)
    
    elif repeat == "day": # Create a recurring event with days_of_week set to None

        crud.create_recur_event(title, all_day, start_time, end_time, "", "", url, display,
                 background_color, border_color, text_color, None, start_recur, end_recur, None, None,
                 completed, user)
    
    else: # Create a recurring event with days_of_week specified

        days_of_week = " ".join(days_of_week)
        
        crud.create_recur_event(title, all_day, start_time, end_time, "", "", url, display,
                 background_color, border_color, text_color, days_of_week, start_recur, end_recur, None, None,
                 completed, user)

    return redirect("/dashboard")


@app.route("/create-routine")
def create_new_routine():
    """Creates a new routine."""
    
    # Get user input for routine
    title = request.args.get("routine-title")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    repeat = request.args.get("routine-repeat-option")
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("routine-repeat-start")
    end_recur = request.args.get("routine-repeat-end")

    # Initalize user and default display settings
    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    if repeat == "day":
        routine = crud.create_routine(title, start_time, end_time, "", "", url, display,
                        background_color, border_color, text_color,
                        None, start_recur, end_recur, None, None,
                        completed, user)
    
    else:
        days_of_week = " ".join(days_of_week)
            
        routine = crud.create_routine(title, start_time, end_time, "", "", url, display,
                            background_color, border_color, text_color,
                            days_of_week, start_recur, end_recur, None, None,
                            completed, user)
    
    # Add actions to routine
    action_titles = request.args.getlist("action-title")

    # TODO: Add more options for user to enter in addition to action title
    for action_title in action_titles:
        crud.create_action(action_title, "", "", "", "", "", "", "", "", "",
                           None, None, False, routine)

    return redirect("/dashboard")


@app.route("/create-tasklist")
def create_new_tasklist():
    """Creates a new tasklist."""
    
    # Get user input for tasklist
    title = request.args.get("tasklist-title")
    date = request.args.get("tasklist-date")
    repeat = request.args.get("repeat-option")
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("event-repeat-start")
    end_recur = request.args.get("event-repeat-end")
    
    all_day = True
    url = "/delete"
    display = "auto"
    background_color = "blue"
    border_color = "black"
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    if repeat == "none": # Create a one-time event
        
        tasklist = crud.create_tasklist(title, all_day, date, url, display, background_color,
                         border_color, text_color, None, None, completed, user)
    
    elif repeat == "day": # Create a recurring event with days_of_week set to None
    
        recur_tasklist = crud.create_recur_tasklist(title, all_day, "", url, display, background_color,
                                   border_color, text_color, None, start_recur, end_recur,
                                   None, None, completed, user)

    else: # Create a recurring event with days_of_week specified

        days_of_week = " ".join(days_of_week)

        recur_tasklist = crud.create_recur_tasklist(title, all_day, "", url, display, background_color,
                                   border_color, text_color, days_of_week, start_recur, end_recur,
                                   None, None, completed, user)

    # Add tasks to tasklist
    task_titles = request.args.getlist("task-title")

    # TODO: Add more options for user to enter in addition to task title
    for task_title in task_titles:
        
        if repeat == "none":
            crud.create_task(task_title, "", "", "", "", None, None, False, tasklist)
        
        else:
            crud.create_recur_task(task_title, "", "", "", "", None, None, False, recur_tasklist)

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
