# import all required libraries
import os
from flask import Flask, redirect, url_for
from models_file.models import db, Account

def init_app():# define a function to initialize the Flask application and configure the database
    app = Flask(__name__)# create a Flask application instance
    base = os.path.abspath(os.path.dirname(__file__))# gets the absolutre path of the current's file directory.
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base, 'gama_v2.sqlite')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False# disable the modification tracking feature of SQLAlchemy to save system resources.
    app.config['SECRET_KEY'] = 'gamma_cyber_dark_42' # sets asecret key for security which protects sessions and form data agnaist tampering.

    db.init_app(app)# initialize the SQLAlchemy instance with the Flask application.
    
    from controllers.auth_ctrl import auth_routes
    from controllers.customer_ctrl import customer_routes
    from controllers.coordinator_ctrl import coordinator_routes
    from controllers.director_ctrl import director_routes

    app.register_blueprint(auth_routes)
    app.register_blueprint(customer_routes,url_prefix='/customer')
    app.register_blueprint(coordinator_routes,url_prefix='/coordinator')
    app.register_blueprint(director_routes,url_prefix='/director')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))# redirect the user to the login page when they access the root URL.
    

if __name__ == '__main__':
    app = init_app()
    with app.app_context():
        db.create_all()
        # Seed default data
        if not Account.query.filter_by(username='director').first():
            a1 = Account(username='director', role_level='director')
            a1.set_pass('director')
            
            a2 = Account(username='gamma_customer', role_level='customer')
            a2.set_pass('password123')
            
            a3 = Account(username='gamma_coord', role_level='coordinator', authorized=True)
            a3.set_pass('password123')
            
            db.session.add_all([a1, a2, a3])
            db.session.commit()
            
    print("Project Gamma Online on port 8113...")
    app.run(debug=True, port=8113)
