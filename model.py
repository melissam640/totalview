"""Models for productivity app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String,
                      unique=True,
                      nullable=False)
    password = db.Column(db.String,
                         nullable=False)
    username = db.Column(db.String)
    theme = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    

class Event(db.Model):
    """A one-time event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    all_day = db.Column(db.Boolean)
    start = db.Column(db.String)
    end = db.Column(db.String)
    start_str = db.Column(db.String)
    end_str = db.Column(db.String)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Event event_id={self.event_id} title={self.title}>"
    

class RecurEvent(db.Model):
    """A recurring event."""

    __tablename__ = "recur_events"

    recur_event_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    all_day = db.Column(db.Boolean)
    start = db.Column(db.String)
    end = db.Column(db.String)
    start_str = db.Column(db.String)
    end_str = db.Column(db.String)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    days_of_week = db.Column(db.String)
    start_recur = db.Column(db.String)
    end_recur = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Recurring Event recur_event_id={self.recur_event_id} title={self.title}>"
    

class Routine(db.Model):
    """A routine."""

    __tablename__ = "routines"

    routine_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    start_str = db.Column(db.String)
    end_str = db.Column(db.String)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    days_of_week = db.Column(db.String)
    start_recur = db.Column(db.String)
    end_recur = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Routine routine_id={self.routine_id} title={self.title}>"
    

class Action(db.Model):
    """An action."""

    __tablename__ = "actions"

    action_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    routine_id = db.Column(db.Integer,
                        db.ForeignKey("routines.routine_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    start_str = db.Column(db.String)
    end_str = db.Column(db.String)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Action action_id={self.action_id} title={self.title}>"
    

class Tasklist(db.Model):
    """A tasklist."""

    __tablename__ = "tasklists"

    tasklist_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    all_day = db.Column(db.Boolean)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Tasklist tasklist_id={self.tasklist_id} title={self.title}>"
    

class RecurTasklist(db.Model):
    """A recurring tasklist."""

    __tablename__ = "recur_tasklists"

    recur_tasklist_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    all_day = db.Column(db.Boolean)
    url = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    days_of_week = db.Column(db.String)
    start_recur = db.Column(db.String)
    end_recur = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Recurring Tasklist recur_tasklist_id={self.recur_tasklist_id} title={self.title}>"
    

class Task(db.Model):
    """A task."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    tasklist_id = db.Column(db.Integer,
                        db.ForeignKey("tasklists.tasklist_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Task task_id={self.task_id} title={self.title}>"
    

class RecurTask(db.Model):
    """A task for a recurring tasklist."""

    __tablename__ = "recur_tasks"

    recur_task_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    recur_tasklist_id = db.Column(db.Integer,
                        db.ForeignKey("recur_tasklists.recur_tasklist_id"))
    # Data for FullCalendar API
    title = db.Column(db.String)
    display = db.Column(db.String)
    background_color = db.Column(db.String)
    border_color = db.Column(db.String)
    text_color = db.Column(db.String)
    # Data for additional formatting
    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Recurring Task recur_task_id={self.recur_task_id} title={self.title}>"
    

def connect_to_db(flask_app, db_uri="postgresql:///productivity", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo=False)