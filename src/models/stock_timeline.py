from dataclasses import dataclass
from datetime import datetime

from .. import db


@dataclass
class StockTimeline(db.Model):
    __tablename__ = "stock_timeline"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    vending_machine_id: int = db.Column(db.Integer, db.ForeignKey("vending_machine.id"), nullable=False)
    quantity: int = db.Column(db.Integer)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "vending_machine_id": self.vending_machine_id,
            "quantity": self.quantity,
            "timestamp": self.timestamp.isoformat(),
        }
