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
    name = db.Column(db.String)
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
    

class Recur_Event(db.Model):
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