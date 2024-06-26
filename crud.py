"""CRUD operations."""

from pandas import date_range
from datetime import datetime, date, timedelta

from model import (db, User, Event, RecurEvent, Routine, Action,
                   Tasklist, RecurTasklist, Task, RecurTask, connect_to_db)


### User account ###


def check_email_exists(email):
    """Checks if user's email was already used to create an account."""

    if User.query.filter_by(email=email).first():
        return True
    
    return False


def create_user(email, password, username):
    """Create a new user account."""

    user = User(email=email, password=password, username=username,
                theme="light", accent_color="#818387",
                profile_pic="/static/profile-pics/default.png")
    
    db.session.add(user)
    db.session.commit()

    return user


def check_credentials(email, password):
    """Checks user's credentials."""

    user = User.query.filter_by(email=email).first()
    
    if user:
        if user.email!=email or user.password!=password:
            return None
        else:
            return user
    
    return None


### Create new calendar items ###


def create_event(title, all_day, start, end, start_str, end_str, url,
                 background_color, border_color, user):
    """Create and return a new event."""

    event = Event(
                title=title,
                all_day=all_day,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                background_color=background_color,
                border_color=border_color,
                user=user
                )

    db.session.add(event)
    db.session.commit()
    
    return event


def create_recur_event(title, all_day, start, end, start_str, end_str, url,
                       background_color, border_color,
                       days_of_week, start_recur, end_recur, user):
    """Create and return a new recurring event."""

    recur_event = RecurEvent(
                title=title,
                all_day=all_day,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                background_color=background_color,
                border_color=border_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                user=user
                )

    db.session.add(recur_event)
    db.session.commit()
    
    return recur_event


def create_routine(title, start, end, start_str, end_str, url,
                   background_color, border_color, days_of_week,
                   start_recur, end_recur, user):
    """Create and return a new routine."""

    routine = Routine(
                title=title,
                start=start,
                end=end,
                start_str=start_str,
                end_str=end_str,
                url=url,
                background_color=background_color,
                border_color=border_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                user=user
                )

    db.session.add(routine)
    db.session.commit()
    
    return routine


def create_action(title, background_color, border_color, completed, routine):
    """Create and return a new action."""

    action = Action(
                title=title,
                background_color=background_color,
                border_color=border_color,
                completed=completed,
                routine=routine
                )

    db.session.add(action)
    db.session.commit()
    
    return action


def create_tasklist(title, all_day, start, url, background_color,
                    border_color, user):
    """Create and return a new tasklist."""

    tasklist = Tasklist(
                title=title,
                all_day=all_day,
                start=start,
                url=url,
                background_color=background_color,
                border_color=border_color,
                user=user
                )

    db.session.add(tasklist)
    db.session.commit()
    
    return tasklist


def create_recur_tasklist(title, all_day, url,
                          background_color, border_color,
                          days_of_week, start_recur, end_recur, user):
    """Create and return a new recurring tasklist."""

    recur_tasklist = RecurTasklist(
                title=title,
                all_day=all_day,
                url=url,
                background_color=background_color,
                border_color=border_color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur,
                user=user
                )

    db.session.add(recur_tasklist)
    db.session.commit()
    
    return recur_tasklist


def create_task(title, background_color, border_color, completed, tasklist):
    """Create and return a new task."""

    task = Task(
                title=title,
                background_color=background_color,
                border_color=border_color,
                completed=completed,
                tasklist=tasklist
                )

    db.session.add(task)
    db.session.commit()
    
    return task


def create_recur_task(title, background_color, border_color,
                    completed, recur_tasklist):
    """Create and return a new recurring task."""

    recur_task = RecurTask(
                title=title,
                background_color=background_color,
                border_color=border_color,
                completed=completed,
                recur_tasklist=recur_tasklist
                )

    db.session.add(recur_task)
    db.session.commit()
    
    return recur_task


### Get by id ###


def get_user_by_id(user_id):
    """Gets user object by id."""

    user = User.query.get(user_id)

    return user


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


def get_tasklist_by_id(tasklist_id):
    """Gets a tasklist by id."""

    tasklist = Tasklist.query.get(tasklist_id)

    return tasklist


def get_task_by_id(task_id):
    """Gets a task by id."""

    task = Task.query.get(task_id)

    return task


def get_recur_tasklist_by_id(recur_tasklist_id):
    """Gets a recurring tasklist by id."""

    recur_tasklist = RecurTasklist.query.get(recur_tasklist_id)

    return recur_tasklist


def get_recur_task_by_id(recur_task_id):
    """Gets a recuring task by id."""

    recur_task = RecurTask.query.get(recur_task_id)

    return recur_task


### Get items for FullCalendar ###


def get_all_calendar_items(user):
    """Gets all calendar items for a user."""

    items = []
    
    for event in Event.query.filter_by(user=user).all():
        items.append({
            "title": event.title,
            "allDay": event.all_day,
            "start": event.start,
            "end": event.end,
            "url": event.url,
            "display": "auto",
            "backgroundColor": event.background_color,
            "borderColor": event.border_color,
            "textColor": "black"
        })
    
    for recur_event in RecurEvent.query.filter_by(user=user).all():
        
        # Convert days_of_week from string to list if it's not None
        if recur_event.days_of_week:
            days_of_week = recur_event.days_of_week.split(" ")
        else:
            days_of_week = recur_event.days_of_week

        # Add one day to end_recur, this date in FullCalendar is not inclusive
        end_recur = add_day_to_date(recur_event.end_recur)
        
        items.append({
            "title": recur_event.title,
            "allDay": recur_event.all_day,
            "startTime": recur_event.start,
            "endTime": recur_event.end,
            "url": recur_event.url,
            "display": "auto",
            "backgroundColor": recur_event.background_color,
            "borderColor": recur_event.border_color,
            "textColor": "black",
            "daysOfWeek": days_of_week,
            "startRecur": recur_event.start_recur,
            "endRecur": end_recur
        })

    for routine in Routine.query.filter_by(user=user).all():
        
        # Convert days_of_week from string to list if it's not None
        if routine.days_of_week:
            days_of_week = routine.days_of_week.split(" ")
        else:
            days_of_week = routine.days_of_week
        
        # Add one day to end_recur, this date in FullCalendar is not inclusive
        end_recur = add_day_to_date(routine.end_recur)
        
        items.append({
            "title": routine.title,
            "startTime": routine.start,
            "endTime": routine.end,
            "url": routine.url,
            "display": "auto",
            "backgroundColor": routine.background_color,
            "borderColor": routine.border_color,
            "textColor": "black",
            "daysOfWeek": days_of_week,
            "startRecur": routine.start_recur,
            "endRecur": end_recur
        })

    for tasklist in Tasklist.query.filter_by(user=user).all():
        
        items.append({
            "title": tasklist.title,
            "allDay": tasklist.all_day,
            "start": tasklist.start,
            "url": tasklist.url,
            "display": "auto",
            "backgroundColor": tasklist.background_color,
            "borderColor": tasklist.border_color,
            "textColor": "black"
        })

    for recur_tasklist in RecurTasklist.query.filter_by(user=user).all():
        
        # Convert days_of_week from string to list if it's not None
        if recur_tasklist.days_of_week:
            days_of_week = recur_tasklist.days_of_week.split(" ")
        else:
            days_of_week = recur_tasklist.days_of_week
        
        # Add one day to end_recur, this date in FullCalendar is not inclusive
        end_recur = add_day_to_date(recur_tasklist.end_recur)
        
        items.append({
            "title": recur_tasklist.title,
            "allDay": recur_tasklist.all_day,
            "url": recur_tasklist.url,
            "display": "auto",
            "backgroundColor": recur_tasklist.background_color,
            "borderColor": recur_tasklist.border_color,
            "textColor": "black",
            "daysOfWeek": days_of_week,
            "startRecur": recur_tasklist.start_recur,
            "endRecur": end_recur
        })

    return items


### Get tasklist items for dashboard page ###


def get_todays_tasklists(user):
    """Gets tasklists assigned to today."""

    todays_date = str(date.today())
    todays_tasklists = []
    
    for tasklist in Tasklist.query.filter_by(user=user).all():

        if tasklist.start == todays_date:
            todays_tasklists.append(tasklist)

    return todays_tasklists


def get_todays_recur_tasklists(user):
    """Gets recurring tasklists assigned to today."""

    todays_date = str(date.today())
    # %7 to convert Sunday to 0 instead of 7 to match FullCalendar
    day_of_week = str(date.today().isoweekday() % 7)
    todays_recur_tasklists = []

    for recur_tasklist in RecurTasklist.query.filter_by(user=user).all():

        recur_tasklist_range = date_range(recur_tasklist.start_recur,
                                          recur_tasklist.end_recur)

        if todays_date in recur_tasklist_range:
            
            if recur_tasklist.days_of_week is None:
                todays_recur_tasklists.append(recur_tasklist)
            
            elif day_of_week in recur_tasklist.days_of_week:
                todays_recur_tasklists.append(recur_tasklist)

    return todays_recur_tasklists


def create_dashboard_tasklist_objects(user):
    """Creates a dictionary of tasklist information for dashboard."""

    tasklists = get_todays_tasklists(user)
    tasklist_objects = []
    
    for tasklist in tasklists: 
        tasklist_objects.append({
            "type": "tasklist",
            "id": tasklist.tasklist_id,
            "title": tasklist.title,
            "url": tasklist.url,
            "tasks": tasklist.tasks,
            "color": tasklist.background_color
        })
    
    return tasklist_objects


def create_dashboard_recur_tasklist_objects(user):
    """Creates a dictionary of recurring tasklist information for dashboard."""

    recur_tasklists = get_todays_recur_tasklists(user)
    recur_tasklist_objects = []
    
    for recur_tasklist in recur_tasklists: 
        recur_tasklist_objects.append({
            "type": "recur_tasklist",
            "id": recur_tasklist.recur_tasklist_id,
            "title": recur_tasklist.title,
            "url": recur_tasklist.url,
            "tasks": recur_tasklist.recur_tasks,
            "color": recur_tasklist.background_color,
        })
    
    return recur_tasklist_objects


def sort_dashboard_tasklist_objects(user):
    """Combines and sorts tasklist items to be displayed on /dashboard."""

    tasklist_objects = create_dashboard_tasklist_objects(user)
    recur_tasklist_objects = create_dashboard_recur_tasklist_objects(user)

    dashboard_objects = []
    dashboard_objects.extend(tasklist_objects)
    dashboard_objects.extend(recur_tasklist_objects)

    return dashboard_objects


### Get event and routine items for dashboard ###


def get_todays_events(user):
    """Gets user events scheduled for today."""

    todays_date = str(date.today())
    todays_events = []
    
    for event in Event.query.filter_by(user=user).all():
        
        event_range = date_range(event.start[:10], event.end[:10])

        if todays_date in event_range:
            todays_events.append(event)

    return todays_events


def get_todays_recur_events(user):
    """Gets user recurring events scheduled for today."""

    todays_date = str(date.today())
    day_of_week = str(date.today().isoweekday() % 7)
    todays_recur_events = []

    for recur_event in RecurEvent.query.filter_by(user=user).all():
        recur_event_range = date_range(recur_event.start_recur,
                                       recur_event.end_recur)
        
        if todays_date in recur_event_range:
            
            if recur_event.days_of_week is None:
                todays_recur_events.append(recur_event)
            
            elif recur_event.days_of_week is not None and day_of_week in recur_event.days_of_week:
                todays_recur_events.append(recur_event)

    return todays_recur_events


def get_todays_routines(user):
    """Gets user routines scheduled for today."""

    todays_date = str(date.today())
    day_of_week = str(date.today().isoweekday() % 7)
    todays_routines = []

    for routine in Routine.query.filter_by(user=user).all():
        routine_range = date_range(routine.start_recur, routine.end_recur)
        
        if todays_date in routine_range:
            
            if routine.days_of_week is None:
                todays_routines.append(routine)
            
            elif routine.days_of_week is not None and day_of_week in routine.days_of_week:
                todays_routines.append(routine)

    return todays_routines


def create_dashboard_event_objects(user):
    """Creates a dictionary of event information for dashboard."""

    events = get_todays_events(user)
    event_objects = []
    
    # Change start_time for all_day events from None to "" for sorting
    for event in events:
        if event.all_day:
            start_time = ""
            end_time = None
        else:
            start_time = event.start[11:]
            end_time = event.end[11:]
        
        event_objects.append({
            "type": "event",
            "id": event.event_id,
            "all_day": event.all_day,
            "start_time": start_time,
            "end_time": end_time,
            "start_str": event.start_str,
            "end_str": event.end_str,
            "time_dif": None,
            "title": event.title,
            "url": event.url,
            "color": event.background_color
        })
    
    return event_objects


def create_dashboard_recur_event_objects(user):
    """Creates a dictionary of recurring event information for /dashboard."""

    recur_events = get_todays_recur_events(user)
    recur_event_objects = []
    
    # Change start_time for all_day events from None to "" for sorting
    for recur_event in recur_events:
        if recur_event.all_day:
            start_time = ""
            end_time = None
        else:
            start_time = recur_event.start
            end_time = recur_event.end
        
        recur_event_objects.append({
            "type": "recur_event",
            "id": recur_event.recur_event_id,
            "all_day": recur_event.all_day,
            "start_time": start_time,
            "end_time": end_time,
            "start_str": recur_event.start_str,
            "end_str": recur_event.end_str,
            "time_dif": None,
            "title": recur_event.title,
            "url": recur_event.url,
            "color": recur_event.background_color
        })
    
    return recur_event_objects


def create_dashboard_routine_objects(user):
    """Creates a dictionary of routine information for /dashboard."""

    routines = get_todays_routines(user)
    routine_objects = []
    
    for routine in routines:
        routine_objects.append({
            "type": "routine",
            "id": routine.routine_id,
            "all_day": False,
            "start_time": routine.start,
            "end_time": routine.end,
            "start_str": military_to_standard_time(routine.start),
            "end_str": military_to_standard_time(routine.end),
            "time_dif": None,
            "title": routine.title,
            "actions": routine.actions,
            "url": routine.url,
            "color": routine.background_color
        })
    
    return routine_objects


def sort_dashboard_event_routine_objects(user):
    """Combines and sorts calendar items to be displayed on /dashboard."""

    event_objects = create_dashboard_event_objects(user)
    recur_event_objects = create_dashboard_recur_event_objects(user)
    routine_objects = create_dashboard_routine_objects(user)

    dashboard_objects = []
    dashboard_objects.extend(event_objects)
    dashboard_objects.extend(recur_event_objects)
    dashboard_objects.extend(routine_objects)

    sorted_dashboard_objects = sorted(dashboard_objects,
                                      key=lambda x: x["start_time"])

    return sorted_dashboard_objects


### Time functions ###


def get_date_str(item_date, item_time):
    """Converts user date and time input into a parsable string."""

    return item_date + "T" + item_time


def add_day_to_date(date_str):
    """Adds one day to dates that are not inclusive in FullCalendar."""

    inital_date = datetime.strptime(date_str, "%Y-%m-%d")

    end_date = (inital_date + timedelta(days=1)).strftime("%Y-%m-%d")

    return end_date


def military_to_standard_time(time_str):
    """Converts time strings from 24hr to standard time."""

    time = datetime.strptime(time_str, "%H:%M")

    standard = time.strftime("%I:%M %p")

    return standard


def find_time_differences(start_str, end_str):
    """Finds the hours and minutes between two time strings."""

    start_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")
    
    delta = end_time - start_time

    hours = int(delta.total_seconds() / 3600)
    if hours < 1:
        minutes = int((delta.total_seconds()) / 60)
        if minutes <= 0:
            return None
        return f"{minutes}m"


    minutes = int((delta.total_seconds() - (hours * 3600)) / 60)
    if minutes < 1:
        return f"{hours}h"

    return f"{hours}h {minutes}m"


def find_time_between_items(dashboard_items):
    """Finds the time between events and routines if any."""

    for i, item in enumerate(dashboard_items):
        if item["all_day"] is False and dashboard_items[i] != dashboard_items[-1]:
            next_item = dashboard_items[i+1]
            
            if next_item["all_day"] is False:
                item["time_dif"] = find_time_differences(item["end_time"],
                                                         next_item["start_time"])
    
    return dashboard_items


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
