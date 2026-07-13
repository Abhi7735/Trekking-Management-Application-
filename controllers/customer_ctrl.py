from flask import Blueprint, render_template, session, redirect, url_for, request
from models.schemas import db, Journey, Ticket

customer_routes = Blueprint('customer', __name__)

@customer_routes.route('/dashboard')
def dashboard():
    if session.get('role') != 'customer': return redirect(url_for('auth.login'))
    q = request.args.get('q', '')
    difficulty = request.args.get('difficulty', '')
    
    # Base query: show treks that are Scheduled or Open
    query = Journey.query.filter(Journey.status.in_(['Scheduled', 'Open']))
    
    # Filter by location search
    if q:
        query = query.filter(Journey.location.ilike(f'%{q}%'))
    
    # Filter by difficulty
    if difficulty:
        query = query.filter(Journey.difficulty == difficulty)
    
    journeys = query.all()
        
    my_tickets = Ticket.query.filter_by(customer_id=session['aid']).all()
    my_jids = [t.journey_id for t in my_tickets]
    return render_template('customer_dash.html', journeys=journeys, my_tickets=my_tickets, my_jids=my_jids, q=q, difficulty=difficulty)

@customer_routes.route('/buy_ticket/<int:jid>', methods=['POST'])
def buy_ticket(jid):
    if session.get('role') != 'customer': return redirect(url_for('auth.login'))
    j = Journey.query.get(jid)
    if j and j.available_slots > 0 and j.status in ('Scheduled', 'Open'):
        j.available_slots -= 1
        t = Ticket(customer_id=session['aid'], journey_id=jid, status='Booked')
        db.session.add(t)
        db.session.commit()
    return redirect(url_for('customer.dashboard'))
