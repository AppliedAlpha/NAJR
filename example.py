from app import db, Seat, Reservation, app
from datetime import datetime

# Ensure operations run within the Flask application context
with app.app_context():
    # Create the database tables if they don't exist
    db.create_all()

    db.session.query(Seat).delete() # Remove all existing seats

    # Insert some test seats
    seat_labels = [f"{region}-{row}열-{num}번" for region in ("A", "B", "C") for row in range(1, 10) for num in range(1, 10)]

    # Remove some seats that don't exist
    for num in range(1, 10):
        seat_labels.remove(f"B-9열-{num}번")
    seat_labels.remove("A-9열-1번")
    seat_labels.remove("A-9열-2번")
    seat_labels.remove("C-9열-8번")
    seat_labels.remove("C-9열-9번")

    region = {'A': 109, 'B': 555, 'C': 997}


    for label in seat_labels:
        existing_seat = Seat.query.filter_by(seat_label=label).first()
        if not existing_seat:  # Prevent duplicates
            _x = 0
            _y = 0

            seat_num = label.split("-")
            _x += region[seat_num[0]] + (int(seat_num[2][0]) - 1) * 39
            _y += 310 + (int(seat_num[1][0]) - 1) * 60

            seat = Seat(seat_label=label, is_reserved=False, x=_x, y=_y)  # All seats start as available
            db.session.add(seat)

    db.session.commit()

    '''
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

    '''
    print("Test data inserted successfully!")