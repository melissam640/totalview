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
        user = crud.create_user(email, password, username)
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
    todays_events_routines = crud.sort_dashboard_objects(user)
    todays_tasklists = crud.get_todays_tasklists(user)

    for i, item in enumerate(todays_events_routines):
        if item["all_day"] is False and todays_events_routines[i] != todays_events_routines[-1]:
            next_item = todays_events_routines[i+1]
            if next_item["all_day"] is False:
                item["time_dif"] = crud.find_time_differences(item["end_time"], next_item["start_time"])
    
    return render_template("dashboard.html", username=user.username,
                           todays_events_routines=todays_events_routines,
                           todays_tasklists=todays_tasklists,
                           theme=user.theme,
                           accent=user.accent_color)

@app.route("/month")
def show_monthly_schedule():
    """Create user monthly schedule."""

    user = crud.get_user_by_id(session["user_id"])

    return render_template("month.html", username=user.username,
                           theme=user.theme,
                           accent=user.accent_color)

@app.route("/settings")
def show_user_settings():
    """Creates page with user theme and accent color options."""

    user = crud.get_user_by_id(session["user_id"])

    return render_template("settings.html", username=user.username,
                           theme=user.theme,
                           accent=user.accent_color)

@app.route("/account")
def show_user_account():
    """Creates page with user account infomation."""

    user = crud.get_user_by_id(session["user_id"])

    return render_template("account.html", username=user.username,
                           theme=user.theme,
                           accent=user.accent_color)

@app.route("/api/add-event")
def add_event():
    """Adds a user-created event to the calendar."""

    user = crud.get_user_by_id(session["user_id"])

    items = crud.get_all_calendar_items(user)

    return jsonify(items)


@app.route("/create-event")
def create_new_event():
    """Creates a new event."""
    
    # Get user input for event
    title = request.args.get("event-title")
    color = request.args.get("event-color")
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
    url = "/edit"
    display = "auto"
    background_color = color
    border_color = color
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])
    
    if all_day == "true":
        all_day = True
    else:
        all_day = False

    if end_recur:
        end_recur = crud.add_day_to_date(end_recur)
    
    if repeat == "none": # Create a one-time event

        start = crud.get_date_str(start_date, start_time)
        end = crud.get_date_str(end_date, end_time)
        
        event = crud.create_event(title, all_day, start, end, "", "", url, display,
                 background_color, border_color, text_color, None, None,
                 completed, user)
        
        event.url = f"/edit/{event.event_id}"
        db.session.commit()
    
    elif repeat == "day": # Create a recurring event with days_of_week set to None

        recur_event = crud.create_recur_event(title, all_day, start_time, end_time, "", "", url, display,
                 background_color, border_color, text_color, None, start_recur, end_recur, None, None,
                 completed, user)
        
        recur_event.url = f"/edit-recur-event/{recur_event.recur_event_id}"
        db.session.commit()
    
    else: # Create a recurring event with days_of_week specified

        days_of_week = " ".join(days_of_week)
        
        recur_event = crud.create_recur_event(title, all_day, start_time, end_time, "", "", url, display,
                 background_color, border_color, text_color, days_of_week, start_recur, end_recur, None, None,
                 completed, user)
        
        recur_event.url = f"/edit-recur-event/{recur_event.recur_event_id}"
        db.session.commit()

    return redirect("/dashboard")


@app.route("/create-routine")
def create_new_routine():
    """Creates a new routine."""
    
    # Get user input for routine
    title = request.args.get("routine-title")
    color = request.args.get("routine-color")
    start_time = request.args.get("routine-start-time")
    end_time = request.args.get("routine-end-time")
    repeat = request.args.get("routine-repeat-option")
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("routine-repeat-start")
    end_recur = request.args.get("routine-repeat-end")

    # Initalize user and default display settings
    url = "/edit-routine"
    display = "auto"
    background_color = color
    border_color = color
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])
    
    if repeat == "day":
        routine = crud.create_routine(title, start_time, end_time, "", "", url, display,
                        background_color, border_color, text_color,
                        None, start_recur, end_recur, None, None,
                        completed, user)
        
        routine.url = f"/edit-routine/{routine.routine_id}"
        db.session.commit()
    
    else:
        days_of_week = " ".join(days_of_week)
            
        routine = crud.create_routine(title, start_time, end_time, "", "", url, display,
                            background_color, border_color, text_color,
                            days_of_week, start_recur, end_recur, None, None,
                            completed, user)
        
        routine.url = f"/edit-routine/{routine.routine_id}"
        db.session.commit()
    
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
    color = request.args.get("tasklist-color")
    date = request.args.get("tasklist-date")
    repeat = request.args.get("repeat-option")
    days_of_week = request.args.getlist("days-of-week")
    start_recur = request.args.get("event-repeat-start")
    end_recur = request.args.get("event-repeat-end")
    
    all_day = True
    url = "/delete"
    display = "auto"
    background_color = color
    border_color = color
    text_color = "black"
    completed = False
    user=crud.get_user_by_id(session["user_id"])

    if repeat == "none": # Create a one-time event
        
        tasklist = crud.create_tasklist(title, all_day, date, url, display, background_color,
                         border_color, text_color, None, None, completed, user)
        
        tasklist.url = f"/edit-tasklist/{tasklist.tasklist_id}"
        db.session.commit()
    
    elif repeat == "day": # Create a recurring event with days_of_week set to None
    
        recur_tasklist = crud.create_recur_tasklist(title, all_day, "", url, display, background_color,
                                   border_color, text_color, None, start_recur, end_recur,
                                   None, None, completed, user)
        
        recur_tasklist.url = f"/edit-recur-tasklist/{recur_tasklist.recur_tasklist_id}"
        db.session.commit()

    else: # Create a recurring event with days_of_week specified

        days_of_week = " ".join(days_of_week)

        recur_tasklist = crud.create_recur_tasklist(title, all_day, "", url, display, background_color,
                                   border_color, text_color, days_of_week, start_recur, end_recur,
                                   None, None, completed, user)
        
        recur_tasklist.url = f"/edit-recur-tasklist/{recur_tasklist.recur_tasklist_id}"
        db.session.commit()

    # Add tasks to tasklist
    task_titles = request.args.getlist("task-title")

    # TODO: Add more options for user to enter in addition to task title
    for task_title in task_titles:
        
        if repeat == "none":
            crud.create_task(task_title, "", "", "", "", None, None, False, tasklist)
        
        else:
            crud.create_recur_task(task_title, "", "", "", "", None, None, False, recur_tasklist)

    return redirect("/dashboard")


@app.route("/account/edit-email", methods = ["POST"])
def update_user_email():
    """Updates the user's email address."""

    new_email = request.form.get("email")
    
    user = crud.get_user_by_id(session["user_id"])

    user.email = new_email
    db.session.commit()

    return redirect("/account")


@app.route("/account/edit-password", methods = ["POST"])
def update_user_password():
    """Updates the user's password."""

    new_password = request.form.get("password")
    
    user = crud.get_user_by_id(session["user_id"])

    user.password = new_password
    db.session.commit()

    return redirect("/account")


@app.route("/account/logout", methods = ["POST"])
def logout():
    """Logs out a user."""

    session.clear()

    return redirect("/")


@app.route("/account/delete-account", methods = ["POST"])
def delete_account():
    """Deletes a user's account."""

    user = crud.get_user_by_id(session["user_id"])

    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/edit/<event_id>")
def show_event_details(event_id):
    """Shows the details for a selected event."""

    user = crud.get_user_by_id(session["user_id"])
    event = crud.get_event_by_id(event_id)
    
    return render_template("edit.html", event=event, username=user.username,
                           theme=user.theme, accent=user.accent_color)


@app.route("/edit/<event_id>/edit-event-title", methods = ["POST"])
def update_event_title(event_id):
    """Updates the title of a given event."""

    title = request.form.get("edit-event-title")

    event_id_int = int(event_id)
    event = crud.get_event_by_id(event_id_int)

    event.title = title
    db.session.commit()
    
    return redirect(f"/edit/{event_id}")


@app.route("/edit/<event_id>/edit-event-time", methods = ["POST"])
def update_event_time(event_id):
    """Updates the time and date of a given event."""

    start_date = request.form.get("start-date")
    start_time = request.form.get("start-time")
    end_date = request.form.get("end-date")
    end_time = request.form.get("end-time")
    all_day = request.form.get("all-day")

    start = crud.get_date_str(start_date, start_time)
    end = crud.get_date_str(end_date, end_time)

    if all_day == "true":
        all_day = True
    else:
        all_day = False
    
    event_id_int = int(event_id)
    event = crud.get_event_by_id(event_id_int)

    event.start = start
    event.end = end
    event.all_day = all_day
    db.session.commit()
    
    return redirect(f"/edit/{event_id}")


@app.route("/edit/<event_id>/delete-event", methods = ["POST"])
def delete_event(event_id):
    """Deletes an event."""

    event_id_int = int(event_id)
    
    event = crud.get_event_by_id(event_id_int)

    db.session.delete(event)
    db.session.commit()
    
    return redirect("/dashboard")


@app.route("/edit-recur-event/<recur_event_id>")
def show_recur_event_details(recur_event_id):
    """Shows the details for a selected recurring event."""

    user = crud.get_user_by_id(session["user_id"])
    recur_event = crud.get_recur_event_by_id(recur_event_id)
    
    return render_template("edit-recur-event.html", recur_event=recur_event,
                           username=user.username, theme=user.theme,
                           accent=user.accent_color)


@app.route("/edit-recur-event/<recur_event_id>/edit-recur-event-title", methods = ["POST"])
def update_recur_event_title(recur_event_id):
    """Updates the title of a given recurring event."""

    title = request.form.get("edit-recur-event-title")

    recur_event = crud.get_recur_event_by_id(int(recur_event_id))

    recur_event.title = title
    db.session.commit()
    
    return redirect(f"/edit-recur-event/{recur_event_id}")


@app.route("/edit-recur-event/<recur_event_id>/edit-recur-event-time", methods = ["POST"])
def update_recur_event_time(recur_event_id):
    """Updates the time and date of a given recurring event."""

    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    all_day = request.form.get("all-day")

    if all_day == "true":
        all_day = True
    else:
        all_day = False
    
    recur_event = crud.get_recur_event_by_id(int(recur_event_id))

    recur_event.start = start_time
    recur_event.end = end_time
    recur_event.all_day = all_day
    db.session.commit()
    
    return redirect(f"/edit-recur-event/{recur_event_id}")


@app.route("/edit-recur-event/<recur_event_id>/edit-event-recurrence", methods = ["POST"])
def update_event_recurrence(recur_event_id):
    """Updates the recurrence of a given recurring event."""

    repeat = request.form.get("event-repeat-option")
    days_of_week = request.form.getlist("days-of-week")
    start_recur = request.form.get("event-repeat-start")
    end_recur = request.form.get("event-repeat-end")
    
    recur_event = crud.get_recur_event_by_id(int(recur_event_id))

    recur_event.start_recur = start_recur
    recur_event.end_recur = end_recur
    
    if repeat == "day":
        recur_event.days_of_week = None
    else:
        days_of_week = " ".join(days_of_week)
        recur_event.days_of_week = days_of_week

    db.session.commit()

    return redirect(f"/edit-recur-event/{recur_event_id}")


@app.route("/edit-recur-event/<recur_event_id>/delete-recur-event", methods = ["POST"])
def delete_recur_event(recur_event_id):
    """Deletes a recurring event."""

    recur_event = crud.get_recur_event_by_id(int(recur_event_id))

    db.session.delete(recur_event)
    db.session.commit()
    
    return redirect("/dashboard")


@app.route("/edit-routine/<routine_id>")
def show_routine_details(routine_id):
    """Shows the details for a selected routine."""

    user = crud.get_user_by_id(session["user_id"])
    routine = crud.get_routine_by_id(routine_id)
    
    return render_template("edit-routine.html", routine=routine,
                           username=user.username, theme=user.theme,
                           accent=user.accent_color)


@app.route("/edit-routine/<routine_id>/edit-routine-title", methods = ["POST"])
def update_routine_title(routine_id):
    """Updates the title of a given routine."""

    title = request.form.get("edit-routine-title")

    routine = crud.get_routine_by_id(int(routine_id))

    routine.title = title
    db.session.commit()
    
    return redirect(f"/edit-routine/{routine_id}")


@app.route("/edit-routine/<routine_id>/edit-routine-time", methods = ["POST"])
def update_routine_time(routine_id):
    """Updates the time of a given routine."""

    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    all_day = request.form.get("all-day")
    
    routine = crud.get_routine_by_id(int(routine_id))

    routine.start = start_time
    routine.end = end_time
    routine.all_day = all_day
    db.session.commit()
    
    return redirect(f"/edit-routine/{routine_id}")


@app.route("/edit-routine/<routine_id>/edit-routine-recurrence", methods = ["POST"])
def update_routine_recurrence(routine_id):
    """Updates the recurrence of a given routine."""

    repeat = request.form.get("routine-repeat-option")
    days_of_week = request.form.getlist("days-of-week")
    start_recur = request.form.get("routine-repeat-start")
    end_recur = request.form.get("routine-repeat-end")
    
    routine = crud.get_routine_by_id(int(routine_id))

    routine.start_recur = start_recur
    routine.end_recur = end_recur
    
    if repeat == "day":
        routine.days_of_week = None
    else:
        days_of_week = " ".join(days_of_week)
        routine.days_of_week = days_of_week

    db.session.commit()

    return redirect(f"/edit-routine/{routine_id}")


@app.route("/edit-routine/<routine_id>/delete-routine", methods = ["POST"])
def delete_routine(routine_id):
    """Deletes a routine."""

    routine = crud.get_routine_by_id(int(routine_id))

    db.session.delete(routine)
    db.session.commit()
    
    return redirect("/dashboard")


@app.route("/edit-routine/<routine_id>/add-action", methods = ["POST"])
def add_action(routine_id):
    """Adds a new action to a routine."""

    action_title = request.form.get("add-action-title")

    routine = crud.get_routine_by_id(int(routine_id))

    # TODO: Add more options for user to enter in addition to action title
    crud.create_action(action_title, "", "", "", "", "", "", "", "", "",
                           None, None, False, routine)
    
    return redirect(f"/edit-routine/{routine_id}")


@app.route("/edit-routine/<routine_id>/<action_id>/delete-action", methods = ["POST"])
def delete_action(routine_id, action_id):
    """Deletes an action."""

    action = crud.get_action_by_id(int(action_id))

    db.session.delete(action)
    db.session.commit()
    
    return redirect(f"/edit-routine/{routine_id}")


@app.route("/edit-tasklist/<tasklist_id>")
def show_tasklist_details(tasklist_id):
    """Shows the details for a selected tasklist."""

    user = crud.get_user_by_id(session["user_id"])
    tasklist = crud.get_tasklist_by_id(tasklist_id)
    
    return render_template("edit-tasklist.html", tasklist=tasklist,
                           username=user.username, theme=user.theme,
                           accent=user.accent_color)


@app.route("/edit-tasklist/<tasklist_id>/edit-tasklist-title", methods = ["POST"])
def update_tasklist_title(tasklist_id):
    """Updates the title of a given tasklist."""

    title = request.form.get("edit-tasklist-title")

    tasklist = crud.get_tasklist_by_id(int(tasklist_id))

    tasklist.title = title
    db.session.commit()
    
    return redirect(f"/edit-tasklist/{tasklist_id}")


@app.route("/edit-tasklist/<tasklist_id>/edit-tasklist-time", methods = ["POST"])
def update_tasklist_time(tasklist_id):
    """Updates the date of a given tasklist."""

    start_date = request.form.get("start-date")
    
    tasklist = crud.get_tasklist_by_id(int(tasklist_id))

    tasklist.start = start_date
    db.session.commit()
    
    return redirect(f"/edit-tasklist/{tasklist_id}")


@app.route("/edit-tasklist/<tasklist_id>/delete-tasklist", methods = ["POST"])
def delete_tasklist(tasklist_id):
    """Deletes a tasklist."""

    tasklist = crud.get_tasklist_by_id(int(tasklist_id))

    db.session.delete(tasklist)
    db.session.commit()
    
    return redirect("/dashboard")


@app.route("/edit-tasklist/<tasklist_id>/add-task", methods = ["POST"])
def add_task(tasklist_id):
    """Adds a new task to a tasklist."""

    task_title = request.form.get("add-task-title")

    tasklist = crud.get_tasklist_by_id(int(tasklist_id))

    # TODO: Add more options for user to enter in addition to task title
    crud.create_task(task_title, "", "", "", "", None, None, False, tasklist)
    
    return redirect(f"/edit-tasklist/{tasklist_id}")


@app.route("/edit-tasklist/<tasklist_id>/<task_id>/delete-task", methods = ["POST"])
def delete_task(tasklist_id, task_id):
    """Deletes a task."""

    task = crud.get_task_by_id(int(task_id))

    db.session.delete(task)
    db.session.commit()
    
    return redirect(f"/edit-tasklist/{tasklist_id}")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>")
def show_recur_tasklist_details(recur_tasklist_id):
    """Shows the details for a selected recurring tasklist."""

    user = crud.get_user_by_id(session["user_id"])
    recur_tasklist = crud.get_recur_tasklist_by_id(recur_tasklist_id)
    
    return render_template("edit-recur-tasklist.html",
                           recur_tasklist=recur_tasklist,
                           username=user.username, theme=user.theme,
                           accent=user.accent_color)


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/edit-recur-tasklist-title", methods = ["POST"])
def update_recur_tasklist_title(recur_tasklist_id):
    """Updates the title of a given recurring tasklist."""

    title = request.form.get("edit-recur-tasklist-title")

    recur_tasklist = crud.get_recur_tasklist_by_id(int(recur_tasklist_id))

    recur_tasklist.title = title
    db.session.commit()
    
    return redirect(f"/edit-recur-tasklist/{recur_tasklist_id}")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/edit-recur-tasklist-time", methods = ["POST"])
def update_recur_tasklist_time(recur_tasklist_id):
    """Updates the date of a given recurring tasklist."""

    start_date = request.form.get("start-date")
    
    recur_tasklist = crud.get_recur_tasklist_by_id(int(recur_tasklist_id))

    recur_tasklist.start = start_date
    db.session.commit()
    
    return redirect(f"/edit-recur-tasklist/{recur_tasklist_id}")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/edit-recur-tasklist-recurrence", methods = ["POST"])
def update_recur_tasklist_recurrence(recur_tasklist_id):
    """Updates the recurrence of a given tasklist."""

    repeat = request.form.get("tasklist-repeat-option")
    days_of_week = request.form.getlist("days-of-week")
    start_recur = request.form.get("tasklist-repeat-start")
    end_recur = request.form.get("tasklist-repeat-end")
    
    recur_tasklist = crud.get_recur_tasklist_by_id(int(recur_tasklist_id))

    recur_tasklist.start_recur = start_recur
    recur_tasklist.end_recur = end_recur
    
    if repeat == "day":
        recur_tasklist.days_of_week = None
    else:
        days_of_week = " ".join(days_of_week)
        recur_tasklist.days_of_week = days_of_week

    db.session.commit()

    return redirect(f"/edit-recur_tasklist/{recur_tasklist_id}")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/delete-recur-tasklist", methods = ["POST"])
def delete_recur_tasklist(recur_tasklist_id):
    """Deletes a recurring tasklist."""

    recur_tasklist = crud.get_recur_tasklist_by_id(int(recur_tasklist_id))

    db.session.delete(recur_tasklist)
    db.session.commit()
    
    return redirect("/dashboard")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/add-recur-task", methods = ["POST"])
def add_recur_task(recur_tasklist_id):
    """Adds a new task to a recurring tasklist."""

    recur_task_title = request.form.get("add-recur_task-title")

    recur_tasklist = crud.get_recur_tasklist_by_id(int(recur_tasklist_id))

    # TODO: Add more options for user to enter in addition to task title
    crud.create_recur_task(recur_task_title, "", "", "", "", None, None, False, recur_tasklist)
    
    return redirect(f"/edit-recur_tasklist/{recur_tasklist_id}")


@app.route("/edit-recur-tasklist/<recur_tasklist_id>/<recur_task_id>/delete-recur-task", methods = ["POST"])
def delete_recur_task(recur_tasklist_id, recur_task_id):
    """Deletes a task for a recurring tasklist."""

    recur_task = crud.get_recur_task_by_id(int(recur_task_id))

    db.session.delete(recur_task)
    db.session.commit()
    
    return redirect(f"/edit-recur_tasklist/{recur_tasklist_id}")


@app.route("/change-theme")
def change_user_theme():
    """Changes the theme for a user to either light or dark mode."""
    
    user = crud.get_user_by_id(session["user_id"])
    
    if user.theme == "light":
        user.theme = "dark"
        db.session.commit()
        return jsonify("dark")
    
    user.theme = "light"
    db.session.commit()
    return jsonify("light")


@app.route("/change-accent-color", methods = ["POST"])
def change_user_accent_color():
    """Changes the color of buttons and links for a user."""
    
    user = crud.get_user_by_id(session["user_id"])
    accent = request.json.get("accent")
    print("*******", accent)
    
    user.accent_color = accent
    db.session.commit()
    return jsonify(accent)


@app.route("/complete-action", methods = ["POST"])
def mark_action_complete():
    """Changes the completed status of an action to True."""
    
    action_id = request.json.get("actionId")
    
    action = crud.get_action_by_id(int(action_id))

    action.completed = True
    db.session.commit()

    return jsonify("action marked complete")


@app.route("/undo-complete-action", methods = ["POST"])
def mark_action_incomplete():
    """Changes the completed status of an action to False."""
    
    action_id = request.json.get("actionId")
    
    action = crud.get_action_by_id(int(action_id))

    action.completed = False
    db.session.commit()

    return jsonify("action marked incomplete")


@app.route("/complete-task", methods = ["POST"])
def mark_task_complete():
    """Changes the completed status of a task to True."""
    
    task_id = request.json.get("taskId")
    
    task = crud.get_task_by_id(int(task_id))

    task.completed = True
    db.session.commit()

    return jsonify("task marked complete")


@app.route("/undo-complete-task", methods = ["POST"])
def mark_task_incomplete():
    """Changes the completed status of a task to False."""
    
    task_id = request.json.get("taskId")
    
    task = crud.get_task_by_id(int(task_id))

    task.completed = False
    db.session.commit()

    return jsonify("task marked incomplete")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
