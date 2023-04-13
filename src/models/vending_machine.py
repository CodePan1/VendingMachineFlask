from dataclasses import dataclass
from typing import List

from .. import db
from . import Product


@dataclass
class VendingMachine(db.Model):
    __tablename__ = "vending_machine"
    __allow_unmapped__ = True
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100))
    location: str = db.Column(db.Text)
    products: List[Product] = db.relationship("Product", backref="vending_machine", cascade="all, delete-orphan")
