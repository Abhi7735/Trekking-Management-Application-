from flask import Blueprint, render_template, session, redirect, url_for, request
from models.schemas import db, Journey, Ticket

coordinator_routes = Blueprint('coordinator', __name__)# this blueprint is used for the coordinator's routes. it will handle all the requests related to the coordinator's dashboard and actions.

@coordinator_routes.route('/dashboard')#this route is used for the coordinator's dashboard. it will show all the journeys assigned to the coordinator. 
def dashboard():
    if session.get('role') != 'coordinator': return redirect(url_for('auth.login'))
    my_journeys = Journey.query.filter_by(assigned_to=session['aid']).all()
    # For each journey, load the list of registered participants (tickets)
    journey_participants = {}
    for j in my_journeys:
        tickets = Ticket.query.filter_by(journey_id=j.jid).all()
        journey_participants[j.jid] = tickets
    return render_template('coordinator_dash.html', journeys=my_journeys, journey_participants=journey_participants)

@coordinator_routes.route('/update_journey/<int:jid>', methods=['POST'])#
def update_journey(jid):
    if session.get('role') != 'coordinator': return redirect(url_for('auth.login'))
    j = Journey.query.get(jid)
    if j and j.assigned_to == session['aid']:
        j.status = request.form.get('status')
        j.available_slots = int(request.form.get('slots'))
        db.session.commit()
    return redirect(url_for('coordinator.dashboard'))
