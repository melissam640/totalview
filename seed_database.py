"""Script to seed database."""

import os

import crud
import model
import server

os.system("dropdb productivity")
os.system("createdb productivity")
model.connect_to_db(server.app)
model.db.create_all()

# Test user 1

# Account
user = crud.create_user("testuser1@test.com", "testpassword1", "test_user_1")
model.db.session.add(user)

# Test events

# One-time set time event
event1 = crud.create_event("Event 1", False, "2024-04-15T14:30", 
                           "2024-04-15T15:30", "April 15th 2024 2:30PM", "April 15th 2024 3:30PM", "/edit/1", "auto",
                           "green", "green", "black", None, None, False, user)
model.db.session.add(event1)

# One-time all day event
event2 = crud.create_event("Event 2", True, "2024-04-16", "2024-04-16", "April 16th 2024", "April 16th 2024",
                           "/edit/2", "auto", "green", "green", "white", None,
                           None, False, user)
model.db.session.add(event2)

# Repeating daily set time event
event3 = crud.create_recur_event("Recur Event 3", False, "14:30", "15:30",
                          "April 17th 2024 2:30PM", "April 20th 2024 3:30PM", "/edit-recur-event/1", "auto", "green", "green", "black",
                          None, "2024-04-17", "2024-04-20", None, None, False,
                          user)
model.db.session.add(event3)

# Repeating weekly set time event
event4 = crud.create_recur_event("Recur Event 4", False, "14:30", "15:30",
                          "April 23rd 2024 2:30PM", "May 3rd 2024 3:30PM", "/edit-recur-event/2", "auto", "green", "green", "black",
                          "2 4", "2024-04-23", "2024-05-03", None, None, False,
                          user)
model.db.session.add(event4)

# Routine
routine = crud.create_routine("Routine", "14:30", "15:30", "April 24th 2024 2:30PM", "April 26th 2024 3:30PM", "/edit-routine/1", "auto",
                              "red", "red", "white", None, "2024-04-24",
                              "2024-04-26", None, None, False, user)
model.db.session.add(routine)

# Action for routine
action1 = crud.create_action("uncompleted action", "", "", "", "", "", "", "", "", "",
                           None, None, False, routine)
model.db.session.add(action1)

# Action for routine
action2 = crud.create_action("completed action", "", "", "", "", "", "", "", "", "",
                           None, None, True, routine)
model.db.session.add(action2)

tasklist = crud.create_tasklist("Tasklist", True, "2024-04-24", "/edit-tasklist/1", "auto", "blue",
                         "blue", "white", None, None, False, user)
model.db.session.add(tasklist)

task1 = crud.create_task("uncompleted task", "", "", "", "", None, None, False, tasklist)
model.db.session.add(task1)

task2 = crud.create_task("completed task", "", "", "", "", None, None, True, tasklist)
model.db.session.add(task2)

model.db.session.commit()
