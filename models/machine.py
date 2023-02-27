from db import db


class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Machine %r>' % self.name
