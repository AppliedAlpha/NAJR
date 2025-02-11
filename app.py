from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, Seat, Reservation
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with actual SMTP server
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'clusterfriends@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db.init_app(app)
mail = Mail(app)

# Health Check
@app.route('/healthz')
def healthz():
	return "OK", 200
	
@app.route('/status', methods=['GET'])
def status():
    try:
        status_code = int(request.args.get('id'))
        
        if 100 <= status_code <= 599:  # Valid HTTP status codes range
            return '', status_code
        else:
            abort(404)
    except (TypeError, ValueError):
        abort(404)

# Home Page (Title)
@app.route('/')
def index():
    return render_template('title.html')

# Reservation Page
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        # print("Raw request data:", request.data)  # Check raw request
        # print("Form data:", request.form)  # Debug form data
        # print("Headers:", request.headers)  # Debug headers

        if not request.form:
            flash('[!] 전송에 실패했습니다.', 'danger')
            return redirect(url_for('reserve'))
        
        print(request.form)
        seat_label = request.form['seat_label']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        rooting_for = request.form['rooting_for']

        if not seat_label or not name or not email or not phone:
            flash('[!] 제대로 입력되지 않은 항목이 있습니다.', 'danger')
            return redirect(url_for('reserve'))

        seat = Seat.query.filter_by(seat_label=seat_label, is_reserved=False).first()
        
        if not seat:
            flash('[!] 좌석이 이미 예약되었거나, 이용할 수 없습니다.', 'danger')
            return redirect(url_for('reserve'))
        
        prev_name_rev = Reservation.query.filter_by(name=name, is_active=True).first()
        prev_email_rev = Reservation.query.filter_by(email=email, is_active=True).first()
        prev_phone_rev = Reservation.query.filter_by(phone=phone, is_active=True).first()
        if prev_name_rev or prev_email_rev or prev_phone_rev:
            flash('[!] 이미 해당 정보로 좌석 예약 이력이 존재합니다.', 'danger')
            return redirect(url_for('reserve'))
        
        new_reservation = Reservation(seat_id=seat.id, name=name, email=email, phone=phone, rooting_for=rooting_for)
        seat.is_reserved = True  # Mark seat as reserved
        db.session.add(new_reservation)
        db.session.commit()

        msg = Message(f"[나름자리] {name} 님의 좌석 예약이 완료되었습니다.",
                      sender='clusterfriends@gmail.com',
                      recipients=[email])
        msg.html = render_template('reservation_email.html', name=name, seat_label=seat_label)
        mail.send(msg)

        flash('[!!] 예약이 성공했습니다. 이메일로 예약 완료 메일이 발송되었습니다.\n메일이 보이지 않는다면 스팸메일함을 확인해주세요.', 'success')
        return redirect(url_for('index'))
    
    seats = Seat.query.all()
    available_seats = len([seat for seat in seats if not seat.is_reserved])
    
    '''
    current_time = datetime.now()
    if current_time < datetime(2025, 2, 13, 0, 0, 0):
        flash('[!] 예약은 서비스 오픈 이후에 가능합니다.', 'danger')
        for seat in seats:
            seat.is_reserved = True
        available_seats = 0
    '''
    
    return render_template('reservation.html', available_seats=available_seats, seats=seats)

# Check & Cancel Page
@app.route('/check', methods=['GET', 'POST'])
def check_reservation():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        if name == os.getenv('ADMIN_NAME') and phone == os.getenv('ADMIN_PHONE'):
            seats = Seat.query.all()
            reservations = Reservation.query.filter_by(is_active=True).all()
            return render_template('rev_list.html', seats=seats, reservations=reservations)

        reservation = Reservation.query.filter_by(name=name, phone=phone, is_active=True).first()
        if not reservation:
            flash('[!] 해당 정보로 존재하는 좌석 예약 이력이 없습니다.', 'danger')
            return redirect(url_for('check_reservation'))

        seats = Seat.query.all()
        return render_template('check_cancel.html', seats=seats, reservation=reservation)

    seats = Seat.query.all()
    return render_template('check_cancel.html', seats=seats, reservation=None)

@app.route('/cancel/<int:reservation_id>/<int:is_admin>', methods=['POST'])
def cancel_reservation(reservation_id, is_admin):
    reservation = Reservation.query.get(reservation_id)
    if reservation and reservation.is_active:
        reservation.is_active = False
        reservation.seat.is_reserved = False
        db.session.commit()
        flash('[!!] 예약을 성공적으로 취소했습니다.', 'success')
    else:
        flash('[!] 예약을 찾을 수 없거나 이미 취소되었습니다.', 'danger')

    if is_admin:
        seats = Seat.query.all()
        reservations = Reservation.query.filter_by(is_active=True).all()
        return render_template('rev_list.html', seats=seats, reservations=reservations)
    
    return redirect(url_for('check_reservation'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)