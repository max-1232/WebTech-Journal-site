from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, User, Entry
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """Register pagina"""
    if request.method == 'POST':
        print("Formulier ontvangen!")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            return make_response("Vul alles in", 400) # type: ignore

        print(f"Data: {username}, {email}")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Deze gebruikersnaam bestaat al!"

        
        # Maak nieuwe gebruiker aan
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hashed password: {hashed_pw}")
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        print("Gebruiker opgeslagen?")

        # Na registratie sturen we ze naar de homepagina
        redirect(url_for('main.home'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if password and user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            return "Inloggen mislukt. Check je gegevens."

    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', "success")
    return redirect(url_for('main.home'))