from flask import Blueprint, render_template, session, redirect, url_for, request
from models_file.models import db, Journey, Ticket

customer_routes = Blueprint('customer', __name__)

@customer_routes.route('/dashboard')
def dashboard():
    if session.get('role')== 'customer':
        return redirect(url_for('auth.login'))
    q= request.args.get('q','')
    if q:
        journeys = Journey.query.filter(Journey.status == 'scheduled', Journey.location.ilike(f'%{q}%')).all()
    else:
        journeys = Journey.query.filter_by(status='scheduled').all()

    my_tickects = Ticket.query.filter_by(customer_id=session['aid']).all()
    my_jids = [t.journey_id for t in my_tickects]
    return render_template('customer_dash.html' , journeys=journeys, my_tickets=my_tickects, my_jids=my_jids, q=q)
                                          
@customer_routes.route('/buy_ticket/<int:jid>', methods=['POST'])
def buy_ticket(jid):
    if session.get('role') != 'customer': return redirect(url_for('auth.login'))
    j = Journey.query.get(jid)
    if j and j.available_slots > 0 and j.status == 'Scheduled':
        j.available_slots -= 1
        t = Ticket(customer_id=session['aid'], journey_id=jid)
        db.session.add(t)
        db.session.commit()
    return redirect(url_for('customer.dashboard'))

# cbdwucdhcbwdj