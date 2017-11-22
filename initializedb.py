"""Script for initializing your database.

Note that dropping your existing tables is an opt-in operation.
If you want to drop tables before you create tables, set an environment
variable called "DEVELOPMENT" to be "True".
"""
from flask_todo.app import db
import os

if bool(os.environ.get('DEVELOPMENT', '')):
    db.drop_all()
db.create_all()
