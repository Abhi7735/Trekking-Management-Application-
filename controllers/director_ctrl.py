from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.schemas import db, Account, Journey, Ticket
from datetime import datetime

director_routes = Blueprint('director', __name__)# this blueprint is used for the director's routes. it will handle all the requests related to the director's dashboard and actions.

@director_routes.route('/dashboard')# this route is used for the director's dashboard. it will show all the journeys, users, coordinators and tickets in the system.
def dashboard():
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    
    search_q = request.args.get('q', '').strip()
    
    # Build filtered queries based on search
    if search_q:
        journeys = Journey.query.filter(
            db.or_(
                Journey.title.ilike(f'%{search_q}%'),
                Journey.location.ilike(f'%{search_q}%'),
                Journey.jid.ilike(f'%{search_q}%')
            )
        ).all()
        users = Account.query.filter(
            Account.role_level != 'director',
            db.or_(
                Account.username.ilike(f'%{search_q}%'),
                Account.aid.ilike(f'%{search_q}%')
            )
        ).all()
    else:
        journeys = Journey.query.all()
        users = Account.query.filter(Account.role_level != 'director').all()
    
    coords = Account.query.filter_by(role_level='coordinator').all()
    all_tickets = Ticket.query.all()
    
    #  its a summary stats (always total, not filtered)
    total_treks = Journey.query.count()
    total_users = Account.query.filter_by(role_level='customer').count()
    total_staff = Account.query.filter_by(role_level='coordinator').count()
    total_bookings = Ticket.query.count()
    
    return render_template('director_dash.html',
        journeys=journeys, users=users, coords=coords, all_tickets=all_tickets,
        total_treks=total_treks, total_users=total_users, total_staff=total_staff,
        total_bookings=total_bookings, search_q=search_q)

@director_routes.route('/add_journey', methods=['POST'])# this route is used for adding a new journey by the director. it will save the journey details in the database.
def add_journey():
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    d1 = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    d2 = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    dur = request.form.get('duration')
    j = Journey(
        title=request.form.get('title'),
        location=request.form.get('location'),
        difficulty=request.form.get('difficulty'),
        total_slots=int(request.form.get('slots')),
        available_slots=int(request.form.get('slots')),
        duration=int(dur) if dur else None,
        start_date=d1,
        end_date=d2,
        assigned_to=request.form.get('coord_id') or None
    )
    db.session.add(j)
    db.session.commit()
    return redirect(url_for('director.dashboard'))

@director_routes.route('/edit_journey/<int:jid>', methods=['GET', 'POST'])# this route is used for editing the journey by the director. it will update the journey details in the database.
def edit_journey(jid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    j = Journey.query.get_or_404(jid)
    if request.method == 'POST':
        j.title = request.form.get('title')
        j.location = request.form.get('location')
        j.difficulty = request.form.get('difficulty')
        j.total_slots = int(request.form.get('slots'))
        j.available_slots = int(request.form.get('available_slots'))
        dur = request.form.get('duration')
        j.duration = int(dur) if dur else None
        j.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        j.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        j.status = request.form.get('status')
        j.assigned_to = request.form.get('coord_id') or None
        db.session.commit()
        return redirect(url_for('director.dashboard'))
    coords = Account.query.filter_by(role_level='coordinator').all()
    return render_template('edit_journey.html', journey=j, coords=coords)

@director_routes.route('/delete_journey/<int:jid>', methods=['POST'])# this route is used for deleting the journey by the director. its also deletes all the tickets associated with that journey.
def delete_journey(jid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    j = Journey.query.get_or_404(jid)
    # Delete associated tickets first
    Ticket.query.filter_by(journey_id=jid).delete()
    db.session.delete(j)
    db.session.commit()
    return redirect(url_for('director.dashboard'))

@director_routes.route('/auth_coord/<int:aid>', methods=['POST'])# this route is used for authorizing the coordinators by the director. 
def auth_coord(aid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    acc = Account.query.get(aid)
    if acc:
        acc.authorized = True
        db.session.commit()
    return redirect(url_for('director.dashboard'))

@director_routes.route('/ban_user/<int:aid>', methods=['POST'])# this route is uesd for banning the user from the system. (it will inactive them)
def ban_user(aid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    acc = Account.query.get(aid)
    if acc:
        acc.is_active = False
        db.session.commit()
    return redirect(url_for('director.dashboard'))

@director_routes.route('/delete_user/<int:aid>', methods=['POST'])# this route is uded for deleting the banned users
def delete_user(aid):
    if session.get('role') != 'director': return redirect(url_for('auth.login'))
    acc = Account.query.get(aid)
    if acc:
        Ticket.query.filter_by(customer_id=aid).delete()  
        db.session.delete(acc)
        db.session.commit()
    return redirect(url_for('director.dashboard'))


        