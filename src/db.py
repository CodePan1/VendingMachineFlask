"""
This module initializes a SQLAlchemy object for connecting to the database.

The `db` object is used throughout the application to
interact with the database and
perform CRUD (create, read, update, delete) operations on its tables.
"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
