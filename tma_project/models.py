from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() # ORM translator between python world and database world



class Account(db.Model):
    __tablename__ = 'accounts'
    aid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passkey = db.Column(db.String(255), nullable=False)
    role_level = db.Column(db.String(20), default='customer') # customer, coordinator, director
    authorized = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

    def set_pass(self, plain):
        self.passkey = generate_password_hash(plain, method='pbkdf2:sha256', salt_length=12)
    
    def check_pass(self, plain):
        return check_password_hash(self.passkey, plain)

class Journey(db.Model):
    __tablename__ = 'journeys'
    jid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Active, Completed
    assigned_to = db.Column(db.Integer, db.ForeignKey('accounts.aid'), nullable=True)
    
    coordinator = db.relationship('Account', backref='journeys_managing', foreign_keys=[assigned_to])

class Ticket(db.Model):
    __tablename__ = 'tickets'
    tid = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('accounts.aid', ondelete='CASCADE'))
    journey_id = db.Column(db.Integer, db.ForeignKey('journeys.jid', ondelete='CASCADE'))
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Account', backref=db.backref('tickets', cascade='all, delete-orphan'), foreign_keys=[customer_id])
    journey = db.relationship('Journey', backref=db.backref('tickets', cascade='all, delete-orphan'))

