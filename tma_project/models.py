from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import UserMixin # type: ignore
from datetime import datetime

db = SQLAlchemy() # ORM translator between python world and database world

class User(db.model, UserMixin):
    __tablename__ = 'Users'
    U_id = db.Column(db.Integer, primary_key = True)
    U_name = db.Column(db.String(100),nullable = False,Unique = True)
    U_email = db.Column(db.String(200),nullable = False, Unique = True)
    U_password = db.Column(db.String(300),nullable = False, Unique= True)
    U_role = db.Column(db.String(50),nullable = False)
    U_created_at = db.Column(db.DateTime , default= datetime.utcnow)
    U_ph_number = db.Column(db.String(40), nullable = False)

    # relationships : User to Booking is one to many
    bookings = db.relationship('Booking', backref='User', lazy=True)

class Trek_staff(db.model):
    __tablename__ = 'Trek_staff'
    s_id = db.Column(db.Integer, primary_key = True)
    s_name = db.Column(db.String(150), nullable = False)
    s_email_id = db.Column(db.String(250), nullable = False, Unique = True)
    staff_ph_number = db.Column(db.String(40),nullable = False)
    s_created_at = db.Column(db.DateTime, default = datetime.utcnow)

# relationships : Trek_staff to Trek is one to many
    Treks = db.relationship('Trek', backref = 'Trek_staff', lazy = True)

class Trek(db.model):
    __tablename__ = 'Treks'
    Tr_id = db.Column(db.Integer, primary_key = True)
    Tr_name = db.Column(db.String(100), nullable= False , unique = True )
    Tr_difficulty = db.Column(db.String(70),nullable = False)
    Tr_duration = db.Column(db.String(100), nullable = False)
    Avail_slots = db.Column(db.Integer, nullable = False)
    Assigned_staff_id = db.Column(db.Integer, db.ForeignKey('Trek_staff.s_id'), nullable = False)
    Tr_status = db.Column(db.String(100), nullable = False,default = 'Pending')
    Tr_location = db.Column(db.String(200), nullable = False)
    Tr_price = db.Column(db.Float, nullable = False)
    Tr_start_date = db.Column(db.DateTime, nullable = False)
    Tr_end_date = db.Column(db.DateTime, nullable = False)

# relationships : Trek to Booking is one to many
    Bookings = db.relationship('Booking', backref = 'Trek', lazy = True)

class Booking(db.model):
    __tablename__ = 'Bookings'
    B_id = db.Column(db.Integer, primary_key = True)
    User_id = db.Column(db.Integer, db.ForeignKey('Users.U_id'), nullable = False)
    Trek_id = db.column(db.integers, db.ForeignKey('Treks.Tr_id'), nullable = False)
    B_status = db.column(db.string(100), nullable = False, default = 'Pending')
    B_date = db.column(db.datetime, default = datetime.utcnow)
    payment_status = db.column(db.string(100), nullable = False, default = 'Pending') 
