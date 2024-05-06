"""Script to seed database with test data."""

import os

import crud
import model
import server

os.system("dropdb productivity")
os.system("createdb productivity")
model.connect_to_db(server.app)
model.db.create_all()

# Test user

# Account
user = crud.create_user("testuser@test.com", "test", "User Name")
model.db.session.add(user)

# Test events

# One-time set time event
event1 = crud.create_event("One-Time Event", False, "2024-05-06T14:30", 
                           "2024-05-06T15:30", "2:30PM", "3:30PM", "/edit-event/1",
                           "green", "green", user)
model.db.session.add(event1)

# One-time all day event
event2 = crud.create_event("All Day Event", True, "2024-05-16", "2024-05-16", None, None,
                           "/edit-event/2", "green", "green", user)
model.db.session.add(event2)

# Repeating daily set time event
event3 = crud.create_recur_event("Daily Recurring Event", False, "14:30", "15:30",
                          "2:30PM", "3:30PM", "/edit-recur-event/1", "green", "green",
                          None, "2024-05-17", "2024-05-20", user)
model.db.session.add(event3)

# Repeating weekly set time event
event4 = crud.create_recur_event("Weekly Recurring Event", False, "14:30", "15:30",
                          "2:30PM", "3:30PM", "/edit-recur-event/2", "green", "green",
                          "2 4", "2024-05-23", "2024-06-03", user)
model.db.session.add(event4)

# Routine
routine = crud.create_routine("Daily Routine", "14:30", "15:30", "2:30PM", "3:30PM", "/edit-routine/1",
                              "red", "red", None, "2024-04-24",
                              "2024-04-26", user)
model.db.session.add(routine)

# Action for routine
action1 = crud.create_action("uncompleted action", None, None, False, routine)
model.db.session.add(action1)

# Action for routine
action2 = crud.create_action("completed action", None, None, True, routine)
model.db.session.add(action2)

tasklist = crud.create_tasklist("Tasklist", True, "2024-05-06", "/edit-tasklist/1", "blue",
                         "blue", user)
model.db.session.add(tasklist)

task1 = crud.create_task("uncompleted task", None, None, False, tasklist)
model.db.session.add(task1)

task2 = crud.create_task("completed task", None, None, True, tasklist)
model.db.session.add(task2)

model.db.session.commit()
