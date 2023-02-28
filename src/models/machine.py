"""This module contains the `Machine` class definition."""

from src.db import db


class Machine(db.Model):
    """Represents a vending machine in the database."""

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), unique=True, nullable=False)
    location: str = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self: "Machine") -> str:
        """Return a string representation of the machine."""
        return f"<Machine {self.name}>"
