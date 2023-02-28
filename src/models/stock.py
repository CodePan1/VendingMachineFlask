"""This module contains the `Stock` class definition."""

from src.db import db


class Stock(db.Model):
    """Represents a stock item for a vending machine in the database."""

    id: int = db.Column(db.Integer, primary_key=True)
    machine_id: int = db.Column(
        db.Integer,
        db.ForeignKey("machine.id"),
        nullable=False,
    )
    product_name: str = db.Column(db.String(80), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)

    def __repr__(self: "Stock") -> str:
        """Return a string representation of the stock item."""
        return (
            f"<Stock(id={self.id}, "
            f"machine_id={self.machine_id}, "
            f"product_name={self.product_name}, "
            f"quantity={self.quantity})>"
        )
