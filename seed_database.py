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
user = crud.create_user("testuser1@test.com", "testpassword1", "test_user_1", "light")
model.db.session.add(user)

# Test events

# One-time set time event
event1 = crud.create_event("Event 1", False, "2024-04-15T14:30:00", 
                           "2024-04-15T15:30:00", "", "", "/delete", "auto",
                           "green", "green", "black", None, None, False, user)
model.db.session.add(event1)

# One-time all day event
event2 = crud.create_event("Event 2", True, "2024-04-16", "2024-04-16", "", "",
                           "/delete", "auto", "green", "green", "white", None,
                           None, False, user)
model.db.session.add(event2)

# Repeating daily set time event
event3 = crud.create_recur_event("Recur Event 3", False, "14:30:00", "15:30:00",
                          "", "", "/delete", "auto", "green", "green", "black",
                          None, "2024-04-17", "2024-04-20", None, None, False,
                          user)
model.db.session.add(event3)

# Repeating weekly set time event
event4 = crud.create_recur_event("Recur Event 4", False, "14:30:00", "15:30:00",
                          "", "", "/delete", "auto", "green", "green", "black",
                          "2 4", "2024-04-23", "2024-05-03", None, None, False,
                          user)
model.db.session.add(event4)

# Routine
routine = crud.create_routine("Routine", "", "", "", "", "/delete", "auto",
                              "red", "red", "white", "2 4", "2024-04-09",
                              "2024-04-12", None, None, False, user)
model.db.session.add(routine)

model.db.session.commit()
