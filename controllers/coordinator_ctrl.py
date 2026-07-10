from flask import Blueprint, render_template, request, redirect, url_for, session
from models_file.models import db, journey

coordinator_routes = Blueprint('coordinator', __name__)

@coordinator_routes.route('/dashboard')
def dashboard():
    if session.get('role') != 'coordinator':
        return redirect(url_for('auth.login'))
    my_journeys = journey.query.filter_by(assigned_to=session['aid']).all()
    return render_template('coordinator_dashboard.html', journeys=my_journeys)

@coordinator_routes.route('/update_journey/<int:jid>', methods=['POST'])
def update_journey(jid):
    if session.get('role') != 'coordinator':
        return redirect(url_for('auth.login'))
    
    j = journey.query.get(jid)
    if j and j.assigned_to == session['aid']:
        j.status = request.form('status')
        j.available_slots = int(request.form.get('slots'))
        db.session.commit()
    return redirect(url_for('coordinator.dashboard'))

        
                                          