"""CRUD operations."""

from datetime import date

from model import (db, User, Event, RecurEvent, Routine, Action, 
                   Tasklist, RecurTasklist, Task, RecurTask, connect_to_db)

def create_user(email, password, username, theme):
    """Create and return a new user."""

    user = User(email=email, password=password, username=username, theme=theme)

    return user


def get_user_by_id(user_id):
    """Gets user object by id."""

    user = User.query.get(user_id)

    return user


def check_credentials(email, password):
    """Checks user's credentials."""

    user = User.query.filter_by(email=email).first()
    
    if user:
        if user.email!=email or user.password!=password:
            return None
        else:
            return user
    else:
        return None
    

def check_email_exists(email):
    """Checks if user's email was already used to create an account."""

    user = User.query.filter_by(email=email).first()
    
    if user:
        return True
    else:
        return False


def create_event(title, all_day, start, end, start_str, end_str, url, display,
                 background_color, border_color, text_color, icon, icon_color,
                 completed, user):
    """Create and return a new event."""

    event = Event(
                title=title,
                all_day=all_day,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                user=user
                )

    db.session.add(event)
    db.session.commit()
    
    return event


def create_recur_event(title, all_day, start, end, start_str, end_str, url,
                       display, background_color, border_color, text_color,
                       days_of_week, start_recur, end_recur, icon, icon_color,
                       completed, user):
    """Create and return a new recurring event."""

    recur_event = RecurEvent(
                title=title,
                all_day=all_day,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                user=user
                )

    db.session.add(recur_event)
    db.session.commit()
    
    return recur_event


def create_routine(title, start, end, start_str, end_str, url, display,
                   background_color, border_color, text_color, days_of_week,
                   start_recur, end_recur, icon, icon_color, completed, user):
    """Create and return a new routine."""

    routine = Routine(
                title=title,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                user=user
                )

    db.session.add(routine)
    db.session.commit()
    
    return routine


def create_action(title, start, end, start_str, end_str, url, display,
                  background_color, border_color, text_color, icon, icon_color,
                  completed, routine):
    """Create and return a new action."""

    action = Action(
                title=title,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                routine=routine
                )

    db.session.add(action)
    db.session.commit()
    
    return action


def create_tasklist(title, all_day, start, url, display, background_color,
                    border_color, text_color, icon, icon_color, completed, user):
    """Create and return a new tasklist."""

    tasklist = Tasklist(
                title=title,
                all_day=all_day,
                start=start,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                user=user
                )

    db.session.add(tasklist)
    db.session.commit()
    
    return tasklist


def create_recur_tasklist(title, all_day, start, url, display,
                          background_color, border_color, text_color,
                          days_of_week, start_recur, end_recur, icon,
                          icon_color, completed, user):
    """Create and return a new recurring tasklist."""

    recur_tasklist = RecurTasklist(
                title=title,
                all_day=all_day,
                start=start,
                url=url,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                user=user
                )

    db.session.add(recur_tasklist)
    db.session.commit()
    
    return recur_tasklist


def create_task(title, display, background_color, border_color, text_color,
                icon, icon_color, completed, tasklist):
    """Create and return a new task."""

    task = Task(
                title=title,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                tasklist=tasklist
                )

    db.session.add(task)
    db.session.commit()
    
    return task


def create_recur_task(title, display, background_color, border_color,
                      text_color, icon, icon_color, completed, recur_tasklist):
    """Create and return a new recurring task."""

    recur_task = RecurTask(
                title=title,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed,
                recur_tasklist=recur_tasklist
                )

    db.session.add(recur_task)
    db.session.commit()
    
    return recur_task


def get_event_by_id(event_id):
    """Gets an event by id."""
    
    event = Event.query.get(event_id)

    return event


def get_recur_event_by_id(recur_event_id):
    """Gets a recurring event by id."""
    
    recur_event = RecurEvent.query.get(recur_event_id)

    return recur_event


def get_routine_by_id(routine_id):
    """Gets a routine by id."""

    routine = Routine.query.get(routine_id)

    return routine


def get_action_by_id(action_id):
    """Gets an action by id."""

    action = Action.query.get(action_id)

    return action


def delete_event(event_title):
    """Deletes an event."""

    event = Event.query.filter(Event.title==event_title).first()

    db.session.delete(event)
    db.session.commit()


def get_todays_tasklists():
    """Gets tasklists assigned to today."""

    todays_date = str(date.today())

    tasklists = Tasklist.query.filter(Tasklist.start==todays_date).all()

    return tasklists


def get_todays_recur_tasklists():
    """Gets recurring tasklists assigned to today."""

    todays_date = str(date.today())

    recur_tasklists = RecurTasklist.query.filter(RecurTasklist.start==todays_date).all()

    return recur_tasklists


def get_todays_events():
    """Gets events assigned to today."""

    todays_date = str(date.today())

    events = Event.query.filter(Event.start.startswith(todays_date)).all()

    return events

def get_todays_recur_events():
    """Gets recurring events assigned to today."""

    todays_date = str(date.today())

    recur_events = RecurEvent.query.filter(RecurEvent.start_recur==todays_date).all()

    return recur_events


def get_todays_routines():
    """Gets routines assigned to today."""

    todays_date = str(date.today())

    routines = Routine.query.filter(Routine.start_recur.startswith(todays_date)).all()

    return routines


def get_date_str(item_date, item_time):
    """Converts user date and time input into a parsable string."""

    return item_date + "T" + item_time


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
