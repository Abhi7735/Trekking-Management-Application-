from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy() # ORM translator between python world and database world



class Account(db.Model): 
    __tablename__ = 'accounts'# tells SQLAlchemy to use this name for the table in the database
    aid = db.Column(db.Integer, primary_key=True)# it is a primary key in autoincreament mode.
    username = db.Column(db.String(80), unique=True, nullable=False)# it contain unique username.
    passkey = db.Column(db.String(255), nullable=False) # its a hashed password.
    role_level = db.Column(db.String(20), default='customer') # customer, coordinator or director.
    authorized = db.Column(db.Boolean, default=True)#(coordinators must be authorised by director).
    is_active = db.Column(db.Boolean, default=True)#(False = banned/blacklisted).
    contact = db.Column(db.String(150), nullable=True) # Staff contact details

    def set_pass(self, plain):# this function takes a normal password and conved into a secured hased password and saved it in selfpasskey.
        self.passkey = generate_password_hash(plain, method='pbkdf2:sha256', salt_length=12)
    
    def check_pass(self, plain):# this function checks whether the password the user entered is correct for this account.
        return check_password_hash(self.passkey, plain)

class Journey(db.Model):
    __tablename__ = 'journeys' # name of the table in the database.
    jid = db.Column(db.Integer, primary_key=True) #primary key.
    title = db.Column(db.String(200), nullable=False)#name of the trekking journey.
    location = db.Column(db.String(100), nullable=False)#Geographic location 
    difficulty = db.Column(db.String(50), nullable=False)#Difficulty level (Easy/Moderate/Hard)
    duration = db.Column(db.Integer, nullable=True)#Duration in days
    total_slots = db.Column(db.Integer, nullable=False)#Total capacity
    available_slots = db.Column(db.Integer, nullable=False)#Remaining available spots
    start_date = db.Column(db.DateTime, nullable=False)#Start date and time of the journey
    end_date = db.Column(db.DateTime, nullable=False)#End date and time of the journey
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Active, Completed
    assigned_to = db.Column(db.Integer, db.ForeignKey('accounts.aid'), nullable=True)#Foreign key → assigned coordinator  
    # one to many relationship. 
    coordinator = db.relationship('Account', backref='journeys_managing', foreign_keys=[assigned_to])

class Ticket(db.Model):
    __tablename__ = 'tickets'# name of the table in the database.
    tid = db.Column(db.Integer, primary_key=True)# primary key
    customer_id = db.Column(db.Integer, db.ForeignKey('accounts.aid', ondelete='CASCADE'))# foreign key → customer who booked the ticket.
    journey_id = db.Column(db.Integer, db.ForeignKey('journeys.jid', ondelete='CASCADE'))# foreign key → journey for which the ticket is booked.
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)# date and time when the ticket was booked.
    status = db.Column(db.String(50), default='Booked') # Booked, Cancelled, Completed
    
    customer = db.relationship('Account', backref=db.backref('tickets', cascade='all, delete-orphan'), foreign_keys=[customer_id])
    journey = db.relationship('Journey', backref=db.backref('tickets', cascade='all, delete-orphan'))

