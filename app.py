from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, Seat, Reservation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with actual SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'

db.init_app(app)
mail = Mail(app)

# Home Page (Title)
@app.route('/')
def index():
    return render_template('title.html')

# Reservation Page
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        seat_label = request.form['seat_label']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        seat = Seat.query.filter_by(seat_label=seat_label, status=False).first()
        
        if not seat:
            flash('Seat is already reserved or does not exist.', 'danger')
            return redirect(url_for('reserve'))
        
        new_reservation = Reservation(seat_id=seat.id, name=name, email=email, phone=phone)
        seat.status = True  # Mark seat as reserved
        db.session.add(new_reservation)
        db.session.commit()

        # Send Email Notification
        msg = Message('Seat Reservation Confirmation',
                      sender='your_email@example.com',
                      recipients=[email])
        msg.body = f"Hello {name},\n\nYour seat {seat_label} has been reserved successfully!"
        mail.send(msg)

        flash('Reservation successful! A confirmation email has been sent.', 'success')
        return redirect(url_for('index'))
    
    seats = Seat.query.filter_by(status=False).all()
    return render_template('reservation.html', seats=seats)

# Check & Cancel Page
@app.route('/check', methods=['GET', 'POST'])
def check_reservation():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']

        reservation = Reservation.query.filter_by(email=email, phone=phone, status=True).first()
        if not reservation:
            flash('No active reservation found with provided details.', 'danger')
            return redirect(url_for('check_reservation'))

        return render_template('check_cancel.html', reservation=reservation)

    return render_template('check_cancel.html', reservation=None)

@app.route('/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation and reservation.status:
        reservation.status = False
        reservation.seat.status = False  # Mark seat as available again
        db.session.commit()
        flash('Reservation canceled successfully.', 'success')
    else:
        flash('Reservation not found or already canceled.', 'danger')

    return redirect(url_for('check_reservation'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)