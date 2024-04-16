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
event1 = crud.create_event("Event Title", False, "2024-04-05T14:30:00", "2024-04-05T15:30:00",
                          "", "", "/", "auto",
                          "green", "white", "black", None, None, False, user)
model.db.session.add(event1)

event2 = crud.create_event("Second Event", True, "2024-04-10", "2024-04-11",
                          "April 10th", "April 11th", "/", "auto",
                          "yellow", "white", "blue", None, None, False, user)
model.db.session.add(event2)

model.db.session.commit()
