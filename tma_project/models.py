from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class User(db.model):
    __tablename__ = 'Users'
    User_id = db.column(db.integers, primary_key = True)
    Username = db.column(db.string(100),nullable = False,Unique = True)
    User_email = db.column(db.string(200),nullable = False, Unique = True)
    User_password = db.column(db.string(300),nullable = False, Unique= True)
    User_role = db.column(db.string(50),nullabe = False)
    User_created_at = db.column(db.datetime , default= datetime.utcnow)

    bookings = db.relationship('Booking', backref='User', lazy=True)

class Trek_staff(db.model):
    __tablename__ = 'Trek_staff'
    staff_id = db.column(db.integers, primary_key = True)
    staff_name = db.column(db.string(150), nullalbe = False)
    staff_email_id = db.column(db.string(250), nullable = False, Unique = True)
    staff_ph_number = db.column(db.string(40),nullable = False)
    staff_created_at = db.column(db.datetime, default = datetime.utcnow)

    Treks = db.relationship('Trek', backref = 'Trek_staff', lazy = True)

class Trek(db.model):
    __tablename__ = 'Treks'
    Trek_id = db.column(db.integers, primary_key = True)
    Trek_name = db.column(db.string(100), nullable= False , unique = True )
    Trek_difficulty = db.column(db.string(70),nullable = False)
    Treck_duration = db.column(db.string(100), nullable = False)
    Avail_slots = db.column(db.integers, nullable = False)
    Assigned_staff_id = db.column(db.integers, db.ForeignKey('Trek_staff.staff_id'), nullable = False)
    Trek_status = db.column(db.string(100), nullable = False,default = 'Pending')
    Trek_location = db.column(db.string(200), nullable = False)

class Booking(db.model):
    __tablename__ = 'Bookings'
    B_id = db.column(db.integers, primary_key = True)
    User_id = db.column(db.integers, db.ForeignKey('Users.U_id'), nullable = False)
    Trek_id = db.column(db.integers, db.ForeignKey('Treks.Tr_id'), nullable = False)
    B_status = db.column(db.string(100), nullable = False, default = 'Pending')
    B_date = db.column(db.datetime, default = datetime.utcnow)
    payment_status = db.column(db.string(100), nullable = False, default = 'Pending') 
