from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class User(db.model):
    __tablename__ = 'Users'
    U_id = db.column(db.integers, primary_key = True)
    U_name = db.column(db.string(100),nullable = False,Unique = True)
    U_email = db.column(db.string(200),nullable = False, Unique = True)
    U_password = db.column(db.string(300),nullable = False, Unique= True)
    U_role = db.column(db.string(50),nullabe = False)
    U_created_at = db.column(db.datetime , default= datetime.utcnow)

    bookings = db.relationship('Booking', backref='User', lazy=True)

class Trek_staff(db.model):
    __tablename__ = 'Trek_staff'
    s_id = db.column(db.integers, primary_key = True)
    s_name = db.column(db.string(150), nullalbe = False)
    s_email_id = db.column(db.string(250), nullable = False, Unique = True)
    staff_ph_number = db.column(db.string(40),nullable = False)
    s_created_at = db.column(db.datetime, default = datetime.utcnow)

    Treks = db.relationship('Trek', backref = 'Trek_staff', lazy = True)

class Trek(db.model):
    __tablename__ = 'Treks'
    Tr_id = db.column(db.integers, primary_key = True)
    Tr_name = db.column(db.string(100), nullable= False , unique = True )
    Tr_difficulty = db.column(db.string(70),nullable = False)
    Tr_duration = db.column(db.string(100), nullable = False)
    Avail_slots = db.column(db.integers, nullable = False)
    Assigned_staff_id = db.column(db.integers, db.ForeignKey('Trek_staff.s_id'), nullable = False)
    Tr_status = db.column(db.string(100), nullable = False,default = 'Pending')
    Tr_location = db.column(db.string(200), nullable = False)

    Bookings = db.relationship('Booking', backref = 'Trek', lazy = True)

class Booking(db.model):
    __tablename__ = 'Bookings'
    B_id = db.column(db.integers, primary_key = True)
    User_id = db.column(db.integers, db.ForeignKey('Users.U_id'), nullable = False)
    Trek_id = db.column(db.integers, db.ForeignKey('Treks.Tr_id'), nullable = False)
    B_status = db.column(db.string(100), nullable = False, default = 'Pending')
    B_date = db.column(db.datetime, default = datetime.utcnow)
    payment_status = db.column(db.string(100), nullable = False, default = 'Pending') 