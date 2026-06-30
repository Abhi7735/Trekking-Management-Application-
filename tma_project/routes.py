# import the necessary libraries and modules
import email

from flask import render_template, request, redirect, session, request, flash
from models import *
from app import app
from datetime import datetime

# homepage route
@app.route('/')
def home():
    return render_template('home.html')

# signup route
@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/signup', methods=('POST'))
def signup_post():
    username = request.form.get('U_name')
    email = request.form.get('U_email')
    password = request.form.get('U_password')
    role = request.form.get('U_role')
    ph_number = request.form.get('U_ph_number')
    gender = request.form.get('U_gender')
    address = request.form.get('U_address')

    Existed_User = User.query.filter((User.U_email == email) | (User.U_name == username))
    
