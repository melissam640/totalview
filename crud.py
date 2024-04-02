"""CRUD operations."""

from model import (db, User, Event, RecurEvent, Routine, Action, 
                   Tasklist, RecurTasklist, Task, RecurTask, connect_to_db)



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
