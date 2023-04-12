from dataclasses import dataclass

from .. import db


@dataclass
class Product(db.Model):
    __tablename__ = "product"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100))
    price: float = db.Column(db.Numeric(precision=5, scale=2))
    quantity: int = db.Column(db.Integer)
    vending_machine_id: int = db.Column(
        db.Integer, db.ForeignKey("vending_machine.id"), nullable=False
    )
