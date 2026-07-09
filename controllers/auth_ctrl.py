from flask import Blueprint, render_template, request, redirect, url_for, session
from models_file.models import db, Account

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form('username')
        p = request.form('password')
        acc = Account.query.filter_by(username=u).first()
        if acc and acc.check_pass(p):
            if not acc.is_active: return render_template('login.html',error="Account banned.")
            if not acc.authorized: return render_template('login.html',error="Account pending authorization.")
            session['aid']= acc.aid
            session['role'] = acc.role_level
            if acc.role_level == 'customer': return redirect(url_for('customer.dashboard'))
            elif acc.role_level == 'coordinator': return redirect(url_for('coordinator.dashboard'))
            elif acc.role_level == 'director': return redirect(url_for('director.dashboard'))
        return render_template('login.html',error="Invalid credentials.")
    return render_template('login.html')

@auth_routes.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form('username')
        p = request.form('password')
        role = request.form('role')
        if Account.query.filter_by(username=u).first():
            return render_template('register.html',error="Username unavailable.")
        
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
            return render_template('login.html',error = 'Registration successful. Await Director approval ')
    return render_template('register.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))    
    