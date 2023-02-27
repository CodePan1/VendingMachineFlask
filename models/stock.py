from db import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Stock(id={self.id}, machine_id={self.machine_id}, product_name={self.product_name}, quantity={self.quantity})>"
