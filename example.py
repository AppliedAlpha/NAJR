from app import db, Seat, Reservation, app
from datetime import datetime

# Ensure operations run within the Flask application context
with app.app_context():
    # Create the database tables if they don't exist
    db.create_all()

    # Insert some test seats
    seat_labels = [
        "A-1열-1번", "A-1열-2번", "A-1열-3번", 
        "A-2열-1번", "A-2열-2번", "A-2열-3번"
    ]

    for label in seat_labels:
        existing_seat = Seat.query.filter_by(seat_label=label).first()
        if not existing_seat:  # Prevent duplicates
            seat = Seat(seat_label=label, is_reserved=False)  # All seats start as available
            db.session.add(seat)

    db.session.commit()

    # Fetch some seats to assign reservations
    seat1 = Seat.query.filter_by(seat_label="A-1열-1번").first()
    seat2 = Seat.query.filter_by(seat_label="A-1열-2번").first()

    if seat1 and seat2:  # Ensure seats exist
        reservation1 = Reservation(
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            seat_id=seat1.id,
            is_active=False,
            reserved_at=datetime.now()
        )

        reservation2 = Reservation(
            name="Jane Smith",
            email="jane@example.com",
            phone="987-654-3210",
            seat_id=seat2.id,
            is_active=True,
            reserved_at=datetime.now()
        )

        # Commit reservations to DB
        db.session.add(reservation1)
        db.session.add(reservation2)
        db.session.commit()

    print("Test data inserted successfully!")