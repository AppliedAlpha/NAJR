from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_label = db.Column(db.String(50), unique=True, nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)  # False = Available, True = Reserved

    def __repr__(self):
        return f"<Seat {self.seat_label}, Reserved: {self.is_reserved}>"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # True = Active, False = Canceled

    seat = db.relationship('Seat', backref=db.backref('reservation', lazy=True))

    def __repr__(self):
        return f"<Reservation {self.name} for {self.seat.seat_label}>"