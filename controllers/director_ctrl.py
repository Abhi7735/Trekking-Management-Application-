from flask import Blueprint, render_template, session, redirect, url_for, request
from models_file.models import db, Account, Journey
from datetime import datetime

director_routes = Blueprint('director', __name__)

@director_routes.route('/dashboard')
def dashboard():
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    journeys = Journey.query.all()
    users = Account.query.filter(Account.role_level != 'director').all()
    coords = Account.query.filter_by(role_level='coordinator').all()
    return render_template('director_dash.html', journeys=journeys, users=users, coords=coords)

@director_routes.route('/add_journey', methods=['POST'])
def add_journey():
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    d1 = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    d2 = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    j = Journey(
        title=request.form.get('title'),
        location=request.form.get('location'),
        difficulty=request.form.get('difficulty'),
        total_slots=int(request.form.get('slots')),
        available_slots=int(request.form.get('slots')),
        start_date=d1,
        end_date=d2,
        assigned_to=request.form.get('coord_id') or None
    )
    db.session.add(j)
    db.session.commit()
    return redirect(url_for('director.dashboard'))

@director_routes.route('/auth_coord/<int:aid>', methods=['POST'])
def auth_coord(aid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    acc = Account.query.get(aid)
    if acc:
        acc.authorized = True
        db.session.commit()
    return redirect(url_for('director.dashboard'))