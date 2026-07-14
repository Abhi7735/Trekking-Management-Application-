from flask import Blueprint, render_template, request, redirect, url_for, session
from models.schemas import db, Account

auth_routes = Blueprint('auth', __name__)# this blueprint is used for the authentication routes. it will handle all the requests related to login, registration and logout.

@auth_routes.route('/login', methods=['GET', 'POST'])# this route is used for the login page. 
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        acc = Account.query.filter_by(username=u).first()
        if acc and acc.check_pass(p):
            if not acc.is_active: return render_template('login.html', error='Account banned.')
            if not acc.authorized: return render_template('login.html', error='Account pending authorization.')
            session['aid'] = acc.aid
            session['role'] = acc.role_level
            if acc.role_level == 'customer': return redirect(url_for('customer.dashboard'))
            elif acc.role_level == 'coordinator': return redirect(url_for('coordinator.dashboard'))
            elif acc.role_level == 'director': return redirect(url_for('director.dashboard'))
        return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])#this route tells user to register for an account. it will save the user details in the database and redirect to the login page
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        role = request.form.get('role')
        if Account.query.filter_by(username=u).first():
            return render_template('register.html', error='Username unavailable.')
        
        is_auth = (role == 'customer')
        new_acc = Account(username=u, role_level=role, authorized=is_auth, is_active=True)
        new_acc.set_pass(p)
        db.session.add(new_acc)
        db.session.commit()
        
        if is_auth:
            session['aid'] = new_acc.aid
            session['role'] = new_acc.role_level
            return redirect(url_for('customer.dashboard'))
        else:
            return render_template('login.html', error='Registration submitted. Await Director approval.')
            
    return render_template('register.html')

@auth_routes.route('/logout')# this route is used for logging out the user from the system. it would clear the session and redirect to the login page.
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
