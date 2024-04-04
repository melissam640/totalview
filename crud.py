"""CRUD operations."""

from model import (db, User, Event, RecurEvent, Routine, Action, 
                   Tasklist, RecurTasklist, Task, RecurTask, connect_to_db)

def create_user(email, password, username, theme):
    """Create and return a new user."""

    user = User(email=email, password=password, username=username, theme=theme)

    return user


def get_user_by_id(id):
    """Gets user object by id."""

    user = User.query.get(id)

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

    return event


def create_recur_event(title, all_day, start, end, start_str, end_str, url,
                       display, background_color, border_color, text_color,
                       days_of_week, start_recur, end_recur, icon, icon_color,
                       completed):
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
                completed=completed
                )

    return recur_event


def create_routine(title, start, end, start_str, end_str, url, display,
                   background_color, border_color, text_color, days_of_week,
                   start_recur, end_recur, icon, icon_color, completed):
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
                completed=completed
                )

    return routine


def create_action(title, start, end, start_str, end_str, url, display,
                  background_color, border_color, text_color, icon, icon_color,
                  completed):
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
                completed=completed
                )

    return action


def create_tasklist(title, all_day, start, url, display, background_color,
                    border_color, text_color, icon, icon_color, completed):
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
                completed=completed
                )

    return tasklist


def create_recur_tasklist(title, all_day, start, url, display,
                          background_color, border_color, text_color,
                          days_of_week, start_recur, end_recur, icon,
                          icon_color, completed):
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
                completed=completed
                )

    return recur_tasklist


def create_task(title, display, background_color, border_color, text_color,
                icon, icon_color, completed):
    """Create and return a new task."""

    task = Task(
                title=title,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed
                )

    return task


def create_recur_task(title, display, background_color, border_color,
                      text_color, icon, icon_color, completed):
    """Create and return a new recurring task."""

    recur_task = RecurTask(
                title=title,
                display=display,
                background_color=background_color,
                border_color=border_color,
                text_color=text_color,
                icon=icon,
                icon_color=icon_color,
                completed=completed
                )

    return recur_task


def delete_event(event_title):
    """Deletes an event."""

    event = Event.query.filter(Event.title==event_title).first()

    db.session.delete(event)
    db.session.commit()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
