from flask import Flask, render_template, url_for, flash, redirect, request, make_response
from models import db, User, Entry
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from routes_entries import entries_bp
from routes_auth import auth_bp
from routes_main import main_bp

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jouw_geheime_code'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Nodig voor het login systeem
login_manager: LoginManager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

# De blueprints voor de routes die in de aparte files staan
app.register_blueprint(entries_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        user1 = User(username="Max", email="max@hanze", password="max") 
        if User.query.count() == 0:
            print("Database is leeg, test-gebruikers toevoegen...")
            
            db.session.add(user1)
            db.session.commit()
            print("Gebruiker succesvol toegevoegd!")
        else:
            print(f"Gebruiker {user1.username} bestaat al")

    app.run(debug=True)